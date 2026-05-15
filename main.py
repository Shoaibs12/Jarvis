import sys
import time
import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject

from audio.hotword import ActivationDetector
from audio.stt import SpeechToText
from audio.tts import TextToSpeech
from agents.coordinator import CoordinatorAgent
from ui.jarvis_ui import JarvisUI
from automation.workflow_engine import engine as workflow_engine

# ------------------------------------------------
# SIGNAL COMMUNICATOR
# ------------------------------------------------
class Communicator(QObject):
    update_status = pyqtSignal(str)
    append_log = pyqtSignal(str)

# ------------------------------------------------
# MAIN JARVIS ENGINE
# ------------------------------------------------
class JarvisEngine:
    def __init__(self, comm):
        print("🔁 Initializing Jarvis...\n")
        self.comm = comm

        self.activation = ActivationDetector("jarvis")
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.brain = CoordinatorAgent()

        # Background thread
        thread = threading.Thread(target=self.core_loop)
        thread.daemon = True
        thread.start()

    def update_ui(self, text):
        self.comm.update_status.emit(text)

    def log_ui(self, text):
        self.comm.append_log.emit(text)

    # --------------------------------------------
    # ACTIVATION -> CONTINUOUS LISTEN
    # --------------------------------------------
    def core_loop(self):
        self.log_ui("[SYSTEM] OS Initialized. Modules loaded.")
        while True:
            self.update_ui("Awaiting Activation...")
            self.log_ui("\n[MIC] Listening for Wake-word or Double Clap...")
            print("\n🎧 Listening for 'Jarvis' or Double Clap...")

            trigger = self.activation.listen()
            if not trigger:
                time.sleep(1)
                continue

            self.update_ui("Activated. Listening...")
            self.log_ui("[SYS] Activation triggered.")
            print("🔈 Jarvis: Yes sir, how can I help?")
            self.tts.speak("Yes sir, how can I help?")
            time.sleep(0.3)

            # Continuous Listening Mode
            listening_active = True
            while listening_active:
                self.update_ui("Listening...")
                print("🎤 Listening... Speak now.")

                user_text = self.stt.listen()

                if not user_text.strip():
                    continue

                print("🗣 You said:", user_text)
                self.update_ui(f"You: {user_text}")
                self.log_ui(f"\n[USER] {user_text}")

                lower_text = user_text.lower()

                # Exit continuous mode commands
                if "sleep" in lower_text or "stop listening" in lower_text:
                    reply = "Entering standby mode, sir."
                    print("🔈 Jarvis:", reply)
                    self.update_ui(f"Jarvis: {reply}")
                    self.log_ui(f"[SYS] {reply}")
                    self.tts.speak(reply)
                    listening_active = False
                    break

                # PROCESS
                self.update_ui("Thinking...")
                self.log_ui("[REASONING] Invoking autonomous tool routing...")

                reply = self.brain.handle(user_text)

                print("🔈 Jarvis:", reply)

                # SPEAK
                self.update_ui(f"Jarvis: {reply}")
                self.log_ui(f"[JARVIS] {reply}")
                self.tts.speak(reply)

                time.sleep(0.5)

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

    engine = JarvisEngine(comm)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
