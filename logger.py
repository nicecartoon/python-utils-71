import logging
import os
from logging.handlers import RotatingFileHandler

GAME_LOG_LEVELS = {
    "COMBAT": 25,
    "QUEST": 26,
    "TELEMETRY": 15,
}

for name, level in GAME_LOG_LEVELS.items():
    logging.addLevelName(level, name)


class GameHudFormatter(logging.Formatter):
    COLORS = {
        "COMBAT": "\u001b[91m",
        "QUEST": "\u001b[93m",
        "TELEMETRY": "\u001b[94m",
        "WARNING": "\u001b[33m",
        "ERROR": "\u001b[31m",
    }
    RESET = "\u001b[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        reset = self.RESET if color else ""
        session_tick = getattr(record, "tick", 0)
        formatted_msg = super().format(record)
        return f"{color}[TICK:{session_tick:08d}] [{record.levelname}] {formatted_msg}{reset}"


def setup_game_logger(
    name: str = "game_engine",
    log_file: str = "logs/game_session.log",
    max_bytes: int = 1048576,
    backup_count: int = 5,
    level: int = logging.DEBUG,
) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(GameHudFormatter("%(message)s"))
    logger.addHandler(console_handler)

    return logger
