import logging
import datetime
from typing import Any

class GamingLogger:
    def __init__(self, name: str = 'GamerLog'):
        self.logger = logging.getLogger(name)
        self._setup()

    def _setup(self) -> None:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] [LEVEL:%(levelname)s] :: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def log_event(self, event_type: str, data: Any) -> None:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        formatted = f'[{timestamp}] EVENT:{event_type.upper()} | DATA:{data}'
        self.logger.info(formatted)

    def critical_fail(self, msg: str) -> None:
        self.logger.critical(f'!!! CRITICAL GAMING FAILURE: {msg} !!!')

log = GamingLogger().log_event
fail = GamingLogger().critical_fail