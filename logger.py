import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


class RpgRarityFormatter(logging.Formatter):
    """Custom formatter mapping log severity to gaming loot rarity tiers."""

    RARITY_TIERS = {
        logging.DEBUG: "[COMMON]",
        logging.INFO: "[UNCOMMON]",
        logging.WARNING: "[RARE]",
        logging.ERROR: "[EPIC]",
        logging.CRITICAL: "[LEGENDARY]",
    }

    def format(self, record: logging.LogRecord) -> str:
        tier = self.RARITY_TIERS.get(record.levelno, "[TRASH]")
        record.rarity = f"{tier:<11}"
        return super().format(record)


def setup_game_logger(
    logger_name: str = "game_session",
    log_dir: str = "logs",
    max_kb: int = 512,
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a rotating log handler tailored for tracking game events."""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{logger_name}.log")

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.hasHandlers():
        return logger

    # Size-based rotation (convert KB to bytes)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_kb * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_fmt = "%(asctime)s %(rarity)s (%(name)s) %(message)s"
    file_handler.setFormatter(RpgRarityFormatter(fmt=file_fmt, datefmt="%H:%M:%S"))
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_fmt = "%(rarity)s %(message)s"
    stream_handler.setFormatter(RpgRarityFormatter(fmt=stream_fmt))
    logger.addHandler(stream_handler)

    return logger
