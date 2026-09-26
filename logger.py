import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name: str = "game_engine") -> logging.Logger:
    """
    Initializes a logger that treats log files like circular buffers,
    essential for capturing performance metrics without disk exhaustion.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_path = os.path.join("logs", f"{name}.log")

    # 5MB per file, keeping 3 backups for historical context
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

# Quick access point for gaming submodules
engine_logger = get_game_logger("core_engine")