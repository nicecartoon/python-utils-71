import logging
from logging.handlers import RotatingFileHandler
import os
import time

class GameTickFormatter(logging.Formatter):
    """
    Custom formatter that injects virtual game ticks (simulated 60fps)
    for frame-accurate debugging diagnostics.
    """
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.start_time = time.time()

    def format(self, record):
        elapsed = time.time() - self.start_time
        current_tick = int(elapsed * 60)
        record.tick = f"TICK:{current_tick:08d}"
        return super().format(record)

def setup_game_logger(
    logger_name: str = "game_engine",
    log_file: str = "game_session.log",
    max_bytes: int = 1048576,
    backup_count: int = 5
) -> logging.Logger:
    """
    Sets up a rotating logger that tracks execution in virtual game ticks.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    format_str = "[%(asctime)s] [%(tick)s] [%(levelname)s] (%(filename)s:%(lineno)d): %(message)s"
    formatter = GameTickFormatter(format_str)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger