import sys
import time
import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject

from speech.hotword import ActivationDetector
from speech.stt import SpeechToText
from speech.tts import TextToSpeech
from agents.coordinator import CoordinatorAgent
from ui.jarvis_ui import JarvisUI

# ------------------------------------------------
# SIGNAL COMMUNICATOR
# ------------------------------------------------
class Communicator(QObject):
    update_status = pyqtSignal(str)

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

    # --------------------------------------------
    # ACTIVATION -> CONTINUOUS LISTEN
    # --------------------------------------------
    def core_loop(self):
        while True:
            self.update_ui("Awaiting Activation...")
            print("\n🎧 Listening for 'Jarvis' or Double Clap...")

            trigger = self.activation.listen()
            if not trigger:
                time.sleep(1)
                continue

            self.update_ui("Activated. Listening...")
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
                    # Check if nothing was said. Give a brief pause and loop again.
                    continue

                print("🗣 You said:", user_text)
                self.update_ui(f"You: {user_text}")

                lower_text = user_text.lower()

                # Exit continuous mode commands
                if "sleep" in lower_text or "stop listening" in lower_text:
                    reply = "Entering standby mode, sir."
                    print("🔈 Jarvis:", reply)
                    self.update_ui(f"Jarvis: {reply}")
                    self.tts.speak(reply)
                    listening_active = False
                    break

                # PROCESS
                self.update_ui("Thinking...")
                reply = self.brain.handle(user_text)
                print("🔈 Jarvis:", reply)

                # SPEAK
                self.update_ui(f"Jarvis: {reply}")
                self.tts.speak(reply)

                # Small pause before listening again
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

    engine = JarvisEngine(comm)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
