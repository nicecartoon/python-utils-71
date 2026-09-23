import logging
from logging.handlers import RotatingFileHandler
import os

def get_gaming_logger(name='game_engine', log_file='game.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | [%(name)s] >> %(message)s')
    
    # Unusual approach: using a lambda to ensure directory existence lazily
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    handler = RotatingFileHandler(
        os.path.join('logs', log_file), 
        maxBytes=1024*1024*5, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    # Prevent duplicate handlers if re-initialized
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Console stream for quick dev debugging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Gaming-specific log singleton instance
game_logger = get_gaming_logger()