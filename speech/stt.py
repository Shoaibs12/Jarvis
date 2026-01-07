import sounddevice as sd
import numpy as np
import whisper
import time

class SpeechToText:
    def __init__(self):
        print("🔁 Loading Whisper model (small)...")
        self.model = whisper.load_model("small")
        print("✅ Whisper loaded")

        self.sr = 16000
        self.silence_threshold = 0.015
        self.max_seconds = 20   # Extended recording window

    def listen(self):
        print("🎤 Listening... Speak now.")

        frames = []
        silent_chunks = 0
        chunk_duration = 0.3
        max_chunks = int(self.max_seconds / chunk_duration)

        with sd.InputStream(samplerate=self.sr, channels=1, dtype='float32'):
            for _ in range(max_chunks):
                audio = sd.rec(int(self.sr * chunk_duration), samplerate=self.sr,
                               channels=1, dtype='float32')
                sd.wait()

                vol = np.abs(audio).mean()

                frames.append(audio)

                if vol < self.silence_threshold:
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                if silent_chunks > 6:  # ~2 seconds of silence
                    break

        audio_np = np.concatenate(frames, axis=0).flatten()

        print("🎧 Transcribing with Whisper...")
        try:
            result = self.model.transcribe(audio_np, fp16=False)
            return result.get("text", "").strip()
        except Exception as e:
            print("❌ Whisper Error:", e)
            return ""
