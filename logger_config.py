"""
Logging configuration for CoastGuard
Centralized logging with file output and console display
"""

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Log file path
LOG_FILE = os.path.join(LOGS_DIR, f"coastguard_{datetime.now().strftime('%Y-%m-%d')}.log")

# Create logger
logger = logging.getLogger("CoastGuard")
logger.setLevel(logging.DEBUG)

# File handler - logs everything to file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Console handler - logs INFO and above to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Add handlers to logger
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"CoastGuard.{name}")
