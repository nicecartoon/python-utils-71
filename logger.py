import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class GameLogger:
    """Creative logger for gaming applications using structured JSON logs and unusual session id."""

    def __init__(self, log_file: str = "game_session.log") -> None:
        self.log_file = log_file
        self.buffer: List[Dict[str, Any]] = []
        self._load_existing_logs()

    def _load_existing_logs(self) -> None:
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        self.buffer.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue

    def log(self, level: str, message: str, **context: Any) -> None:
        entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": message,
            "context": context,
            "session_id": id(self)
        }
        self.buffer.append(entry)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def info(self, message: str, **context: Any) -> None:
        self.log("info", message, **context)

    def warning(self, message: str, **context: Any) -> None:
        self.log("warning", message, **context)

    def error(self, message: str, **context: Any) -> None:
        self.log("error", message, **context)

    def game_event(self, event_type: str, description: str, **data: Any) -> None:
        self.log("game", f"{event_type}: {description}", **data)

    def get_recent_logs(self, count: int = 10) -> List[Dict[str, Any]]:
        return self.buffer[-count:] if self.buffer else []

    def filter_by_level(self, level: str) -> List[Dict[str, Any]]:
        level = level.upper()
        return [entry for entry in self.buffer if entry.get("level") == level]

    def flush_buffer(self) -> None:
        self.buffer = []

    def cleanup_old_sessions(self, max_entries: int = 1000) -> None:
        if len(self.buffer) > max_entries:
            self.buffer = self.buffer[-max_entries:]
            with open(self.log_file, "w") as f:
                for entry in self.buffer:
                    f.write(json.dumps(entry) + "\n")

logger = GameLogger()

def get_logger() -> GameLogger:
    return logger