import logging
from logging.handlers import RotatingFileHandler
import sys

LOOT_LEVEL = 25
QUEST_LEVEL = 35
DEATH_LEVEL = 45

logging.addLevelName(LOOT_LEVEL, "LOOT")
logging.addLevelName(QUEST_LEVEL, "QUEST")
logging.addLevelName(DEATH_LEVEL, "DEATH")

class GameLogger(logging.Logger):
    def loot(self, message, *args, **kws):
        if self.isEnabledFor(LOOT_LEVEL):
            self._log(LOOT_LEVEL, message, args, **kws)

    def quest(self, message, *args, **kws):
        if self.isEnabledFor(QUEST_LEVEL):
            self._log(QUEST_LEVEL, message, args, **kws)

    def death(self, message, *args, **kws):
        if self.isEnabledFor(DEATH_LEVEL):
            self._log(DEATH_LEVEL, message, args, **kws)

logging.setLoggerClass(GameLogger)

class ArcadeFormatter(logging.Formatter):
    def format(self, record):
        symbols = {
            "LOOT": "💎 [LOOT]",
            "QUEST": "⚔️ [QUEST]",
            "DEATH": "💀 [DEATH]",
            "INFO": "ℹ️ [INFO]",
            "WARNING": "⚠️ [WARN]",
            "ERROR": "🚨 [ERROR]"
        }
        prefix = symbols.get(record.levelname, f"[{record.levelname}]")
        original_msg = record.msg
        record.msg = f"{prefix} {original_msg}"
        formatted = super().format(record)
        record.msg = original_msg
        return formatted

def setup_game_logger(log_file="game_session.log", max_bytes=5*1024*1024, backup_count=5):
    logger = logging.getLogger("RetroArcade")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    formatter = ArcadeFormatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger