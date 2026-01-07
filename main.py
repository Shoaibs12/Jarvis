import time
import threading

from speech.hotword import HotwordDetector
from speech.stt import SpeechToText
from speech.tts import TextToSpeech
from agents.coordinator import CoordinatorAgent


# ------------------------------------------------
# MAIN JARVIS ENGINE (NO UI VERSION)
# ------------------------------------------------
class JarvisEngine:
    def __init__(self):
        print("🔁 Initializing Jarvis...\n")

        self.hotword = HotwordDetector("jarvis")
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.brain = CoordinatorAgent()

        # Background thread
        thread = threading.Thread(target=self.core_loop)
        thread.daemon = True
        thread.start()

    # --------------------------------------------
    # HOTWORD → LISTEN → PROCESS → SPEAK
    # --------------------------------------------
    def core_loop(self):
        while True:
            print("\n🎧 Listening for 'Jarvis'...")
            self.hotword.listen()

            print("🔈 Jarvis: Yes sir, how can I help?")
            self.tts.speak("Yes sir, how can I help?")
            time.sleep(0.3)

            # LISTEN
            print("🎤 Listening... Speak now.")
            user_text = self.stt.listen()

            if not user_text.strip():
                print("❌ Could not understand speech.")
                self.tts.speak("I didn't catch that, sir. Please repeat.")
                continue

            print("🗣 You said:", user_text)

            # PROCESS
            reply = self.brain.handle(user_text)
            print("🔈 Jarvis:", reply)

            # SPEAK
            self.tts.speak(reply)

            print("\n🎧 Listening for 'Jarvis' again...\n")


# ------------------------------------------------
# APP ENTRY
# ------------------------------------------------
def main():
    JarvisEngine()

    # Keep program alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
