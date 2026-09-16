import logging
from logging.handlers import RotatingFileHandler
import sys

class RPGFormatter(logging.Formatter):
    """Custom formatter mapping standard log levels to RPG loot tiers."""
    TIER_MAP = {
        logging.DEBUG: "[COMMON] ⚔️ ",
        logging.INFO: "[UNCOMMON] 🛡️ ",
        logging.WARNING: "[RARE] 🔥 ",
        logging.ERROR: "[EPIC] ⚡ ",
        logging.CRITICAL: "[LEGENDARY] 👑 "
    }

    def format(self, record):
        tier = self.TIER_MAP.get(record.levelno, "[UNKNOWN] 🌀 ")
        record.levelname = tier
        return super().format(record)

def setup_game_logger(name="game_engine", log_file="adventure.log", max_mb=2, backups=5):
    """
    Sets up a logger with rotating file mechanics mimicking inventory slot limits.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    max_bytes = int(max_mb * 1024 * 1024)

    # Rotating handler mimicking auto-sorting backpack
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backups,
        encoding="utf-8"
    )

    # Stream handler for immediate output feedback
    console_handler = logging.StreamHandler(sys.stdout)

    log_format = "%(asctime)s | %(levelname)s | %(message)s"
    formatter = RPGFormatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("game logger initialized with automatic log rotation")
    return logger