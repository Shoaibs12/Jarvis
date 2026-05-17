from abc import ABC, abstractmethod
from core.logger import get_logger

logger = get_logger("ActivationEngine")

class ActivationEngine(ABC):
    """
    Abstract base class for all wake-word / activation systems.
    """

    @abstractmethod
    def start(self):
        """Initializes the engine."""
        pass

    @abstractmethod
    def stop(self):
        """Stops and cleans up the engine."""
        pass

    @abstractmethod
    def listen(self) -> str:
        """
        Listens for the trigger event.
        Returns the trigger type (e.g., 'wake_word', 'double_clap', 'manual') or None.
        """
        pass
