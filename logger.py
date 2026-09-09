import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_game_logger(log_name='game_engine', file_path='engine.log'):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] :: %(message)s')
    
    file_handler = RotatingFileHandler(
        file_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

class GamingLogger:
    def __init__(self, name='core'):
        self.log = setup_game_logger(name)

    def critical_hit(self, msg):
        self.log.info(f'CRITICAL EVENT: {msg}')

    def glitch_detected(self, msg):
        self.log.warning(f'GLITCH WARNING: {msg}')