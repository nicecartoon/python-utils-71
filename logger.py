import logging
from logging.handlers import RotatingFileHandler
import os

def setup_game_logger(name: str = 'game_engine', log_dir: str = 'logs'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    path = os.path.join(log_dir, f'{name}.log')
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

    # Unusual approach: using a circular buffer of 5MB files
    handler = RotatingFileHandler(
        path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # Add a console stream for real-time debugging during development
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate standard engine logger
game_logger = setup_game_logger()