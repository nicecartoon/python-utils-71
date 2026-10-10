import logging
import os
from logging.handlers import RotatingFileHandler

def setup_game_logger(name='python-utils-71', log_file='game_state.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d | %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    log = setup_game_logger()
    log.info('game engine initialization sequence started')