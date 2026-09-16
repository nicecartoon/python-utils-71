import logging
from logging.handlers import RotatingFileHandler

class GameStateFilter(logging.Filter):
    def __init__(self, default_zone='WORLD_1'):
        super().__init__()
        self.default_zone = default_zone

    def filter(self, record):
        if not hasattr(record, 'zone'):
            record.zone = self.default_zone
        if not hasattr(record, 'hp'):
            record.hp = 100
        return True

def setup_game_logger(log_file='quest_log.sav', max_megabytes=2, backup_slots=3):
    logger = logging.getLogger('QuestEngine')
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    max_bytes = max_megabytes * 1024 * 1024
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_slots,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] [Zone: %(zone)s] [HP: %(hp)d%%] [%(levelname)s] -> %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addFilter(GameStateFilter())
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

if __name__ == '__main__':
    log = setup_game_logger()
    log.info('Player spawned in the tavern')
    log.warning('Local goblin camp alerted!', extra={'zone': 'GOBLIN_CAVE', 'hp': 85})
    log.error('Boss dragon unleashed fire breath!', extra={'zone': 'DRAGON_LAIR', 'hp': 12})