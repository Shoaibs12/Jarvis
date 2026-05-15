import numpy as np
import sounddevice as sd
import time
from activation.base import ActivationEngine
from core.logger import get_logger

logger = get_logger("OpenWakeWord")

class OpenWakeWordEngine(ActivationEngine):
    def __init__(self, keyword="alexa"):
        self.keyword = keyword
        self.oww_model = None
        self.sample_rate = 16000
        self.chunk_size = 1280

        self.clap_threshold = 0.15
        self.clap_interval_min = 0.2
        self.clap_interval_max = 0.9

    def start(self):
        try:
            # Lazy load OpenWakeWord so a missing dependency doesn't crash the boot
            import openwakeword
            from openwakeword.model import Model
            openwakeword.utils.download_models()
            self.oww_model = Model(wakeword_models=[self.keyword], inference_framework="onnx")
            logger.info(f"OpenWakeWord initialized with keyword: {self.keyword}")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenWakeWord (This is not fatal): {e}")
            self.oww_model = None

    def stop(self):
        self.oww_model = None
        logger.info("OpenWakeWord engine stopped.")

    def is_clap(self, audio_data):
        audio_float = audio_data.astype(np.float32) / 32768.0
        peak = np.max(np.abs(audio_float))
        if peak < self.clap_threshold:
            return False

        fft_data = np.abs(np.fft.rfft(audio_float))
        low_energy = np.sum(fft_data[:10])
        high_energy = np.sum(fft_data[10:])

        if high_energy > low_energy * 0.5:
            return True
        return False

    def listen(self) -> str:
        last_clap_time = 0
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                dtype='int16',
                channels=1
            ) as stream:
                while True:
                    pcm_raw, overflow = stream.read(self.chunk_size)
                    pcm = np.frombuffer(pcm_raw, dtype=np.int16)

                    if self.oww_model:
                        prediction = self.oww_model.predict(pcm)
                        for mdl in self.oww_model.prediction_buffer.keys():
                            if self.oww_model.prediction_buffer[mdl][-1] > 0.5:
                                logger.info(f"🎤 Wake-word detected: {mdl}")
                                return "wake_word"

                    if self.is_clap(pcm):
                        current_time = time.time()
                        if last_clap_time > 0:
                            interval = current_time - last_clap_time
                            if self.clap_interval_min <= interval <= self.clap_interval_max:
                                logger.info("👏 Double Clap detected!")
                                return "double_clap"
                            else:
                                last_clap_time = current_time
                        else:
                            last_clap_time = current_time
                        time.sleep(0.05)

        except Exception as e:
            logger.warning(f"Audio listening failed in OpenWakeWord engine: {e}")
            return None
