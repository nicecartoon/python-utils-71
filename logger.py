import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name='pixel_dev', log_path='logs/game.log'):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    
    file_handler = RotatingFileHandler(
        log_path, maxBytes=1048576, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Dynamic monkey-patching for gaming events
def debug_event(self, msg, *args, **kwargs):
    self.debug(f'GAME_EVENT: {msg}', *args, **kwargs)

logging.Logger.event = debug_event