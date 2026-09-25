import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name: str = 'gaming_core'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, f'{name}.log')
    
    # rotating handler: max 5MB, keep 3 backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)
        
    return logger

# initialized logger for global game state
game_log = get_game_logger('engine')