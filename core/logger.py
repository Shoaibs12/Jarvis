import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Define the root logger format and handlers
logger = logging.getLogger("JARVIS")
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s')

# File Handler
file_handler = RotatingFileHandler("logs/jarvis.log", maxBytes=5 * 1024 * 1024, backupCount=2)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger(name):
    """Utility to get a child logger."""
    return logger.getChild(name)
