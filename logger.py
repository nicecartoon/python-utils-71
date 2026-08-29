import logging
import os
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

class GameEventFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "time": datetime.utcnow().isoformat() + "Z",
            "lvl": record.levelname,
            "msg": record.getMessage(),
            "src": record.module,
            "sess": getattr(record, "game_sess", "main")
        }
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        return json.dumps(log_data)

def setup_game_logger(log_name="game_logger", file_path="logs/game.log", size_limit=5242880, backups=4):
    logger = logging.getLogger(log_name)
    if logger.hasHandlers():
        return logger
    logger.setLevel(logging.DEBUG)
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    rot_handler = RotatingFileHandler(file_path, maxBytes=size_limit, backupCount=backups)
    rot_handler.setFormatter(GameEventFormatter())
    logger.addHandler(rot_handler)
    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(err_handler)
    return logger

def record_game_event(logger, message, data=None, lvl=logging.INFO):
    extra = {"game_sess": datetime.now().strftime("%Y%m%d%H%M")}
    if data:
        extra["extra_data"] = data
    logger.log(lvl, message, extra=extra)