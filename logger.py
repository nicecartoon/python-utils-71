import logging

class GameLogger:
    def __init__(self, name='GameLogger', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.FileHandler('game.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, msg):
        self.logger.info(msg)

    def log_warning(self, msg):
        self.logger.warning(msg)

    def log_error(self, msg):
        self.logger.error(msg)

    def log_debug(self, msg):
        self.logger.debug(msg)

if __name__ == '__main__':
    game_logger = GameLogger()
    game_logger.log_info('Game started')
    game_logger.log_warning('Low health warning')
    game_logger.log_error('Player crashed')
    game_logger.log_debug('State variables initialized')