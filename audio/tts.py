import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play

class TextToSpeech:
    def __init__(self, voice="en-US-ChristopherNeural", rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def _generate(self, text, file="voice.mp3"):
        communicate = edge_tts.Communicate(
            text, voice=self.voice, rate=self.rate, volume=self.volume
        )
        await communicate.save(file)
        return file

    def speak(self, text):
        print(f"🔊 Jarvis Speaking ({self.voice}): {text}")

        async def run_tts():
            file = await self._generate(text)
            audio = AudioSegment.from_file(file)
            play(audio)

        asyncio.run(run_tts())
