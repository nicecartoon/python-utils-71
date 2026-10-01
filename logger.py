import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name: str = 'python-utils-71', log_file: str = 'game_engine.log') -> logging.Logger:
    """
    A slightly over-engineered logger to capture game ticks and errors.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Rotating log mechanism: 5MB per file, keep 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        
        # Custom formatting that makes errors pop out in the console
        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a stream handler for real-time development feedback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Instantiate game-wide logger instance
engine_logger = get_game_logger()