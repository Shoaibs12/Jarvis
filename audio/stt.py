import sounddevice as sd
import numpy as np
import whisper
from core.logger import get_logger

logger = get_logger("STT")

class SpeechToText:
    def __init__(self):
        self.model = None
        self.sr = 16000
        self.silence_threshold = 0.015
        self.max_seconds = 20

    def start(self):
        try:
            logger.info("🔁 Loading Whisper model (small)...")
            self.model = whisper.load_model("small")
            logger.info("✅ Whisper loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper: {e}")
            self.model = None

    def listen(self):
        if not self.model:
            logger.warning("STT Model not loaded. Returning empty string.")
            return ""

        print("🎤 Listening... Speak now.")
        logger.info("Listening for speech...")

        frames = []
        silent_chunks = 0
        chunk_duration = 0.3
        chunk_size = int(self.sr * chunk_duration)
        max_chunks = int(self.max_seconds / chunk_duration)
        has_spoken = False

        try:
            with sd.InputStream(samplerate=self.sr, channels=1, blocksize=chunk_size, dtype='float32') as stream:
                for _ in range(max_chunks):
                    audio_chunk, overflow = stream.read(chunk_size)
                    audio_chunk = audio_chunk.flatten()

                    vol = np.abs(audio_chunk).mean()
                    frames.append(audio_chunk)

                    if vol > self.silence_threshold:
                        has_spoken = True
                        silent_chunks = 0
                    else:
                        if has_spoken:
                            silent_chunks += 1

                    if has_spoken and silent_chunks > 6:
                        break
        except Exception as e:
            logger.error(f"❌ Microphone Error in STT: {e}")
            return ""

        if not frames:
            return ""

        audio_np = np.concatenate(frames, axis=0)

        if np.abs(audio_np).mean() < self.silence_threshold * 0.5:
            return ""

        logger.info("🎧 Transcribing with Whisper...")
        try:
            result = self.model.transcribe(audio_np, fp16=False)
            return result.get("text", "").strip()
        except Exception as e:
            logger.error(f"❌ Whisper Transcription Error: {e}")
            return ""
