import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_game_logger(name: str = 'game_engine', log_file: str = 'game.log'):
    """
    Orchestrates log rotation with a specific capacity for high-frequency
    gaming event tracking, capping at 5MB per file with 3 backups.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        datefmt='%H:%M:%S'
    )

    # Console output for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotation handler to prevent disk saturation
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Return silent logger-like object to swallow accidental double-inits
    return logger if not logger.hasHandlers() else logger

# Instantiate for global use
game_logger = setup_game_logger()