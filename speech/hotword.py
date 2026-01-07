import pvporcupine
import sounddevice as sd
import numpy as np
from config.porcupine_key import PORCUPINE_ACCESS_KEY


class HotwordDetector:
    def __init__(self, keyword="jarvis"):

        try:
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=[keyword]
            )
        except Exception as e:
            raise Exception(f"❌ Porcupine initialization failed: {e}")

        # Audio input configuration
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length

        # Show microphone device
        try:
            device_info = sd.query_devices(kind='input')
            print(f"🎤 Using microphone: {device_info['name']}")
        except:
            print("⚠️ Could not detect microphone device.")

    def listen(self):
        print("🎧 Listening for 'Jarvis'...")

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.frame_length,
                dtype='int16',
                channels=1
            ) as stream:

                while True:
                    pcm = stream.read(self.frame_length)[0]
                    pcm = np.frombuffer(pcm, dtype=np.int16)

                    # Detect hotword
                    result = self.porcupine.process(pcm)
                    if result >= 0:
                        print("🎤 Hotword detected: JARVIS")
                        return True

        except Exception as e:
            print(f"❌ Hotword listening error: {e}")
            return False
