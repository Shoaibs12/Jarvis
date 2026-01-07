import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

# Default audio settings — safe & stable
SAMPLE_RATE = 16000
CHANNELS = 1


def record_audio(duration=5, filename="input.wav"):
    """
    Records raw microphone audio and saves it as a WAV file.
    Safe for Whisper and testing.
    """

    print(f"🎤 Recording for {duration} seconds...")

    try:
        audio = sd.rec(
            int(SAMPLE_RATE * duration),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='float32'
        )
        sd.wait()

        audio = np.squeeze(audio)

        # Save as 16-bit PCM WAV (standard format)
        write(filename, SAMPLE_RATE, (audio * 32767).astype(np.int16))

        print(f"📁 Audio saved to {filename}")
        return filename

    except Exception as e:
        print("⚠️ Microphone error:", e)
        return None


def test_microphone():
    """
    Records a 2-second sample to confirm audio input works.
    """
    print("🎧 Testing microphone...")
    result = record_audio(2, "mic_test.wav")

    if result:
        print("🎉 Microphone test complete — file saved as mic_test.wav")
    else:
        print("❌ Microphone test failed.")
