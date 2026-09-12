import logging
from logging.handlers import RotatingFileHandler
import sys

class GamingLogFormatter(logging.Formatter):
    """Custom log formatter rendering log records as RPG event logs."""
    LEVEL_ICONS = {
        logging.DEBUG: "[LOOT]",
        logging.INFO: "[QUEST]",
        logging.WARNING: "[HAZARD]",
        logging.ERROR: "[WIPE]",
        logging.CRITICAL: "[GAME OVER]"
    }

    def format(self, record):
        icon = self.LEVEL_ICONS.get(record.levelno, "[EVENT]")
        record.msg = f"{icon} {record.msg}"
        return super().format(record)

def setup_game_logger(name="game_core", log_file="game.log", max_megabytes=5, backup_count=3):
    """Configures a rotating logger tuned for game telemetry and debugging."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    max_bytes = max_megabytes * 1024 * 1024
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    
    formatter = GamingLogFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
