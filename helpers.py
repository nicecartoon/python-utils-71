import logging
import os
from logging.handlers import RotatingFileHandler

def setup_game_logger(name: str = 'game_engine', log_dir: str = 'logs') -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        datefmt='%H:%M:%S'
    )

    log_path = os.path.join(log_dir, f'{name}.log')
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

# Dynamic injection of game status reporting
class GameLoggerContext:
    def __init__(self, logger):
        self.logger = logger

    def __enter__(self):
        self.logger.info('--- Session Started ---')
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.critical(f'Crashed: {exc_val}')
        self.logger.info('--- Session Terminated ---')