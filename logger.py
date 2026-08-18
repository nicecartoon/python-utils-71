import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', max_bytes=10485760, backup_count=5):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()

if __name__ == '__main__':
    logger.info('Logger setup complete.')
    logger.debug('This is a debug message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is critical!')