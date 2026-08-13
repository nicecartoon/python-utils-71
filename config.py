import logging
import logging.handlers

def setup_logger(log_file='game.log', max_bytes=10**6, backup_count=3):
    logger = logging.getLogger('GameLogger')
    logger.setLevel(logging.DEBUG)
    
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    my_logger = setup_logger()
    my_logger.debug('Debugging mode activated')
    my_logger.info('Logger is set up and running')
    my_logger.warning('Warning: Check game performance')
    my_logger.error('An error occurred')
    my_logger.critical('Critical issue encountered')