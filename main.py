import sys
import time
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject

import config.features as features
from core.logger import get_logger
from activation.manual_engine import ManualEngine
from activation.openwakeword_engine import OpenWakeWordEngine
from audio.stt import SpeechToText
from audio.tts import TextToSpeech
from agents.coordinator import CoordinatorAgent
from ui.jarvis_ui import JarvisUI
from automation.workflow_engine import engine as workflow_engine

logger = get_logger("SystemManager")

# ------------------------------------------------
# SIGNAL COMMUNICATOR
# ------------------------------------------------
class Communicator(QObject):
    update_status = pyqtSignal(str)
    append_log = pyqtSignal(str)

# ------------------------------------------------
# SERVICE LOADER & MANAGER
# ------------------------------------------------
class SystemManager:
    """Handles the safe initialization of all Jarvis modules."""
    def __init__(self, comm):
        self.comm = comm
        self.activation = None
        self.stt = None
        self.tts = None
        self.brain = None

    def log_status(self, component, status, message):
        tag = "[OK]" if status else "[WARNING]"
        log_line = f"{tag} {component}: {message}"
        print(log_line)
        logger.info(log_line)
        self.comm.append_log.emit(log_line)

    def boot(self):
        """Starts all subsystems with graceful fallbacks."""
        self.comm.append_log.emit("\n[SYSTEM] Boot Sequence Initiated...")

        # 1. Activation Engine
        if features.DEV_MODE:
             self.activation = ManualEngine(simulate=True)
             self.log_status("Activation", False, "DEV_MODE active. Bypassing Wake-Word.")
        elif features.ENABLE_WAKEWORD:
             self.activation = OpenWakeWordEngine(keyword="alexa")
        else:
             self.activation = ManualEngine()
             self.log_status("Activation", False, "Wake-Word disabled in config. Manual mode active.")

        try:
             self.activation.start()
             if not features.DEV_MODE and features.ENABLE_WAKEWORD:
                  self.log_status("Activation", True, "OpenWakeWord Loaded")
        except Exception as e:
             self.log_status("Activation", False, f"Wake-Word Engine Failed ({e}). Falling back to Manual.")
             self.activation = ManualEngine()
             self.activation.start()

        # 2. TTS Engine
        self.tts = TextToSpeech()
        if not features.ENABLE_TTS:
            self.tts.enabled = False
            self.log_status("TTS", False, "TTS Disabled in config")
        else:
            try:
                self.tts.start()
                self.log_status("TTS", True, "TTS Loaded")
            except Exception as e:
                self.log_status("TTS", False, f"TTS Failed to Load ({e})")
                self.tts.enabled = False

        # 3. STT Engine
        self.stt = SpeechToText()
        if not features.ENABLE_STT:
            self.log_status("STT", False, "STT Disabled in config")
        else:
             try:
                 self.stt.start()
                 if self.stt.model is None:
                     self.log_status("STT", False, "STT Model Failed. Voice interaction will be degraded.")
                 else:
                     self.log_status("STT", True, "Whisper Loaded")
             except Exception as e:
                 self.log_status("STT", False, f"STT Exception: {e}")

        # 4. Brain / Coordinator
        try:
             self.brain = CoordinatorAgent()
             self.log_status("Brain", True, "Coordinator Agent Loaded")
        except Exception as e:
             self.log_status("Brain", False, f"Coordinator Agent Failed: {e}")

        # 5. Workflow Engine
        self.log_status("Workflow", True, "Workflow Engine Loaded")

        self.comm.append_log.emit("[SYSTEM] Boot Sequence Complete.\n")

# ------------------------------------------------
# MAIN JARVIS ENGINE (Daemon Worker)
# ------------------------------------------------
class JarvisEngine:
    def __init__(self, comm, ui):
        self.comm = comm
        self.ui = ui
        self.manager = SystemManager(comm)

        # UI Hooks for manual triggers & text input
        self.ui.manual_activation_triggered.connect(self.trigger_manual_activation)
        self.ui.text_input_submitted.connect(self.handle_text_input)

        self.manual_trigger_flag = False

        # Background thread
        thread = threading.Thread(target=self.core_loop)
        thread.daemon = True
        thread.start()

    def update_ui(self, text):
        self.comm.update_status.emit(text)

    def log_ui(self, text):
        self.comm.append_log.emit(text)

    def trigger_manual_activation(self):
        """Called by the UI Activate button."""
        self.manual_trigger_flag = True

    def handle_text_input(self, text):
        """Called by the UI text input box, bypassing voice STT entirely."""
        self.log_ui(f"\n[USER_TEXT] {text}")
        if self.manager.brain:
            self.update_ui("Thinking...")
            reply = self.manager.brain.handle(text)
            self.update_ui(f"Jarvis: {reply}")
            self.log_ui(f"[JARVIS] {reply}")
            self.manager.tts.speak(reply)
        else:
            self.log_ui("[ERROR] Brain offline.")

    def process_voice_input(self):
        """Inner continuous listening loop."""
        listening_active = True
        while listening_active:
            self.update_ui("Listening...")
            print("🎤 Listening... Speak now.")

            # Use STT. If it fails or is disabled, it will return "" fast.
            # We break instead of continuing immediately to prevent CPU loop pegging
            user_text = self.manager.stt.listen()

            if not user_text.strip():
                if features.DEV_MODE or not features.ENABLE_STT or self.manager.stt.model is None:
                    # Prevent infinite busy loop if hardware is missing
                    time.sleep(1)
                    break
                else:
                    continue

            print("🗣 You said:", user_text)
            self.update_ui(f"You: {user_text}")
            self.log_ui(f"\n[USER_VOICE] {user_text}")

            lower_text = user_text.lower()

            if "sleep" in lower_text or "stop listening" in lower_text:
                reply = "Entering standby mode, sir."
                print("🔈 Jarvis:", reply)
                self.update_ui(f"Jarvis: {reply}")
                self.log_ui(f"[SYS] {reply}")
                self.manager.tts.speak(reply)
                listening_active = False
                break

            if self.manager.brain:
                self.update_ui("Thinking...")
                self.log_ui("[REASONING] Invoking autonomous tool routing...")
                reply = self.manager.brain.handle(user_text)
            else:
                reply = "My core reasoning engine is offline. I cannot process that."

            print("🔈 Jarvis:", reply)
            self.update_ui(f"Jarvis: {reply}")
            self.log_ui(f"[JARVIS] {reply}")
            self.manager.tts.speak(reply)

            time.sleep(0.5)

    def core_loop(self):
        self.manager.boot()

        while True:
            self.update_ui("Awaiting Activation...")

            # Check for manual UI click
            if self.manual_trigger_flag:
                self.manual_trigger_flag = False
                trigger = "ui_button"
            else:
                if features.DEV_MODE:
                    self.log_ui("\n[DEV_MODE] Auto-triggering activation in 3 seconds...")
                    trigger = self.manager.activation.listen()
                else:
                    trigger = self.manager.activation.listen()

                    # If hardware fails inside listen(), it might return None quickly. Prevent loop pegging.
                    if trigger is None:
                        time.sleep(1)

            if not trigger:
                continue

            self.update_ui("Activated. Listening...")
            self.log_ui(f"[SYS] Activation triggered via {trigger}.")
            print("🔈 Jarvis: Yes sir, how can I help?")
            self.manager.tts.speak("Yes sir, how can I help?")
            time.sleep(0.3)

            # Enter continuous mode
            self.process_voice_input()

# ------------------------------------------------
# APP ENTRY
# ------------------------------------------------
def main():
    app = QApplication(sys.argv)

    ui = JarvisUI()
    ui.show()

    comm = Communicator()
    comm.update_status.connect(ui.set_status)
    comm.append_log.connect(ui.append_log)

    engine = JarvisEngine(comm, ui)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
