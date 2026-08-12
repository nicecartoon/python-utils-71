import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='game.log', max_bytes=5*1024*1024, backup_count=5):
    logger = logging.getLogger('game_logger')
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Example Usage
if __name__ == '__main__':
    log = setup_logger()
    log.debug('This is a debug message')
    log.info('Game has started')
    log.warning('This is a warning message')
    log.error('An error has occurred')
    log.critical('Critical issue!')
