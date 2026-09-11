import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name='game_logger', log_file='game_log.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [PID:%(process)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File rotation handler with byte limit constraint
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        
        # Console output for real-time debugging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Dynamic log initialization based on current execution context
log = get_game_logger()