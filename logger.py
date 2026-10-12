import logging
from logging.handlers import RotatingFileHandler
import os

def setup_gaming_logger(name='game_engine', log_file='game.log', level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # ensure logs folder exists to keep workspace tidy
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # rotate logs at 5MB, keeping 3 backups
    handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=5*1024*1024,
        backupCount=3
    )
    
    # custom formatting for better game state visibility
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # avoid duplicate handlers in long-running processes
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

# global log instance for the engine
engine_logger = setup_gaming_logger()