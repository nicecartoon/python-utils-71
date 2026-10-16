import logging
from logging.handlers import RotatingFileHandler
import os

def setup_game_logger(name: str = 'python-utils-71', log_file: str = 'game_engine.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] {%(levelname)s} (%(module)s) -> %(message)s',
        datefmt='%H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

if __name__ == '__main__':
    # Example usage for gaming engine debug trace
    game_log = setup_game_logger()
    game_log.info('Engine core initialized - ready for player input')