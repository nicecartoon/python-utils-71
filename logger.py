import logging
from logging.handlers import RotatingFileHandler
import os

def setup_game_logger(name='pixel_forge', log_path='logs/game.log'):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # 5MB per file, keeping 3 backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger

# Quick access point for gaming components
log = setup_game_logger()