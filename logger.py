import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='game.log', max_bytes=10*1024*1024, backup_count=5):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger('game_logger')
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Example usage:
if __name__ == '__main__':
    log = setup_logger()
    log.debug('Debugging information')
    log.info('Game started successfully')
    log.warning('This is a warning message')
    log.error('An error has occurred')
    log.critical('Critical issue!')