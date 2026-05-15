import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
from core.logger import get_logger

logger = get_logger("TTS")

class TextToSpeech:
    def __init__(self, voice="en-US-ChristopherNeural", rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.enabled = True

    def start(self):
        # We could test edge_tts or simple playback here to ensure functionality
        logger.info("✅ TTS engine initialized")

    async def _generate(self, text, file="voice.mp3"):
        try:
            communicate = edge_tts.Communicate(
                text, voice=self.voice, rate=self.rate, volume=self.volume
            )
            await communicate.save(file)
            return file
        except Exception as e:
            logger.error(f"❌ EdgeTTS generation error: {e}")
            return None

    def speak(self, text):
        if not self.enabled:
            logger.info(f"🔊 (Muted) Jarvis: {text}")
            return

        print(f"🔊 Jarvis Speaking: {text}")
        logger.info(f"Speaking: {text}")

        async def run_tts():
            file = await self._generate(text)
            if file:
                try:
                    audio = AudioSegment.from_file(file)
                    play(audio)
                except Exception as e:
                    logger.error(f"❌ Audio playback error: {e}")

        try:
            asyncio.run(run_tts())
        except Exception as e:
             logger.error(f"❌ Async TTS error: {e}")
