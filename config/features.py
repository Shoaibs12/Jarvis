import os

# ----------------------------------------------------
# SYSTEM FEATURE FLAGS
# ----------------------------------------------------
DEV_MODE = os.environ.get("DEV_MODE", "False") == "True"

# Audio & Voice Subsystems
ENABLE_WAKEWORD = os.environ.get("ENABLE_WAKEWORD", "True") == "True"
ENABLE_CLAP_DETECTION = os.environ.get("ENABLE_CLAP_DETECTION", "True") == "True"
ENABLE_TTS = os.environ.get("ENABLE_TTS", "True") == "True"
ENABLE_STT = os.environ.get("ENABLE_STT", "True") == "True"

# If Dev Mode is enabled, force bypass fragile hardware dependencies for quick testing
if DEV_MODE:
    ENABLE_WAKEWORD = False
    ENABLE_CLAP_DETECTION = False
