import time
from activation.base import ActivationEngine
from core.logger import get_logger

logger = get_logger("ManualEngine")

class ManualEngine(ActivationEngine):
    """
    Fallback activation engine.
    In a real desktop environment, this might bind to a hotkey via the 'keyboard' library.
    For cross-platform safety, it simply waits or mimics a console prompt.
    """
    def __init__(self, simulate=False):
        self.simulate = simulate

    def start(self):
        logger.info("Manual Engine initialized. Pressing SPACE (mocked) or triggering via UI needed.")

    def stop(self):
        logger.info("Manual Engine stopped.")

    def listen(self) -> str:
        logger.info("Waiting for manual activation...")
        if self.simulate:
            # Simulate a manual trigger after 3 seconds for dev mode
            time.sleep(3)
            return "manual"

        # In a real GUI, this loop would yield and wait for a UI button click event or a global hotkey.
        # Here we just sleep to avoid pegging the CPU, returning None so the event loop continues.
        time.sleep(1)
        return None
