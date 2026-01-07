# -----------------------------------
# Global Settings for Jarvis Project
# -----------------------------------

# -----------------------------
# Whisper Settings
# -----------------------------
# Model options: tiny, base, small, medium
WHISPER_MODEL = "base"   # best speed + accuracy for local CPU

SAMPLE_RATE = 16000      # Whisper default sample rate
CHANNELS = 1             # Mono microphone input

# -----------------------------
# STT Recording Settings
# -----------------------------
FRAME_DURATION = 0.3     # 300 ms per listening frame
SILENCE_THRESHOLD = 700   # Lower = more sensitive
SILENCE_LIMIT = 1.0       # Stop recording after 1 second of silence

# -----------------------------
# Hotword Detection
# -----------------------------
HOTWORD = "jarvis"        # Built-in Porcupine keyword
# Custom hotword models (.ppn) can be added later

# -----------------------------
# TTS Settings
# -----------------------------
TTS_RATE = 170            # pyttsx3 speaking speed
TTS_VOLUME = 1.0          # Max volume
TTS_VOICE_ID = None       # Default voice (system decides)

# -----------------------------
# File Paths
# -----------------------------
AUDIO_INPUT_FILE = "input.wav"   # Temporary speech input file
MIC_TEST_FILE = "mic_test.wav"   # For debugging microphone
TTS_OUTPUT_FILE = "tts_output.wav"  # Reserved for future UI

# -----------------------------
# Logging Settings
# -----------------------------
DEBUG_MODE = True        # Enables extra terminal output
