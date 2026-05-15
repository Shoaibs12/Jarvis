import pvporcupine
import sounddevice as sd
import numpy as np
import time
from config.porcupine_key import PORCUPINE_ACCESS_KEY

class ActivationDetector:
    def __init__(self, keyword="jarvis"):
        try:
            # Initialize Porcupine for Wake-word
            self.porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=[keyword]
            )
        except Exception as e:
            raise Exception(f"❌ Porcupine initialization failed: {e}")

        # Audio input configuration based on Porcupine's requirement
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length

        # Clap detection settings
        self.clap_threshold = 0.15      # Adjust based on mic sensitivity
        self.clap_interval_min = 0.2    # Min seconds between claps
        self.clap_interval_max = 0.9    # Max seconds between claps

        # Show microphone device
        try:
            device_info = sd.query_devices(kind='input')
            print(f"🎤 Using microphone: {device_info.get('name', 'Unknown')}")
        except:
            print("⚠️ Could not detect microphone device.")

    def is_clap(self, audio_data):
        """
        Detects if an audio chunk contains a clap based on amplitude and frequency.
        """
        # Convert to float for analysis
        audio_float = audio_data.astype(np.float32) / 32768.0
        peak = np.max(np.abs(audio_float))

        if peak < self.clap_threshold:
            return False

        # FFT analysis to check frequency distribution
        fft_data = np.abs(np.fft.rfft(audio_float))
        # Simple energy comparison: claps have higher frequency energy
        low_energy = np.sum(fft_data[:10])   # Low frequencies
        high_energy = np.sum(fft_data[10:])  # High frequencies

        # Avoid false positives from bass-heavy noises
        if high_energy > low_energy * 0.5:
            return True

        return False

    def listen(self):
        """
        Listens continuously until either the wake-word 'Jarvis' is spoken,
        or a double clap is detected.
        """
        print("🎧 Listening for 'Jarvis' or Double Clap...")
        last_clap_time = 0

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.frame_length,
                dtype='int16',
                channels=1
            ) as stream:
                while True:
                    pcm_raw, overflow = stream.read(self.frame_length)
                    pcm = np.frombuffer(pcm_raw, dtype=np.int16)

                    # 1. Wake-word Detection (Porcupine)
                    result = self.porcupine.process(pcm)
                    if result >= 0:
                        print("🎤 Hotword detected: JARVIS")
                        return "wake_word"

                    # 2. Clap Detection
                    if self.is_clap(pcm):
                        current_time = time.time()

                        if last_clap_time > 0:
                            interval = current_time - last_clap_time
                            if self.clap_interval_min <= interval <= self.clap_interval_max:
                                print("👏 Double Clap detected!")
                                return "double_clap"
                            else:
                                # Too fast or too slow, update last_clap_time
                                last_clap_time = current_time
                        else:
                            last_clap_time = current_time

                        # Prevent immediate consecutive detections within the chunk
                        # by ignoring claps for a short period. The while loop runs fast.
                        # Wait a bit or let interval filtering handle it.
                        time.sleep(0.05)

        except Exception as e:
            print(f"❌ Activation listening error: {e}")
            return None
