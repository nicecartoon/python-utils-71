import logging
from typing import Optional, Any

class GameLogger:
    """
    A logger for game-related events.
    """  
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """
        Initializes the logger with a specified name and log level.
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message: str, *args: Any) -> None:
        """
        Logs an info message.
        """
        self.logger.info(message, *args)

    def log_warning(self, message: str, *args: Any) -> None:
        """
        Logs a warning message.
        """
        self.logger.warning(message, *args)

    def log_error(self, message: str, *args: Any) -> None:
        """
        Logs an error message.
        """
        self.logger.error(message, *args)

    def log_critical(self, message: str, *args: Any) -> None:
        """
        Logs a critical message.
        """
        self.logger.critical(message, *args)

# Example usage:
if __name__ == '__main__':
    game_logger = GameLogger('MyGame')
    game_logger.log_info('Game started')
    game_logger.log_warning('Low health warning')
    game_logger.log_error('An error occurred')
    game_logger.log_critical('Critical failure!')
