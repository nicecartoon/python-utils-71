import sys
import datetime
from typing import Any

class GameLogger:
    def __init__(self, prefix: str = '[GAMELOG]'):
        self.prefix = prefix
        self.levels = {'INFO': '🌿', 'WARN': '⚠️', 'CRIT': '💥'}

    def __call__(self, msg: Any, level: str = 'INFO') -> None:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        icon = self.levels.get(level, '🔹')
        print(f"{self.prefix} {timestamp} {icon} {msg}", file=sys.stderr)

    def panic(self, msg: str) -> None:
        self(f"FATAL ERROR: {msg.upper()}", 'CRIT')
        sys.exit(1)

    def silent_log(self, *args: Any) -> None:
        try:
            with open('game_debug.log', 'a') as f:
                print(f"{datetime.datetime.now()}: {args}", file=f)
        except OSError:
            pass

def log_event(message: str, level: str = 'INFO') -> None:
    logger = GameLogger()
    logger(message, level)