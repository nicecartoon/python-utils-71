import sys
from typing import Any

class CombatLogger:
    """A visual, dynamic log processor for real-time RPG combat events."""

    SYMBOLS = {
        "damage": "⚔️",
        "heal": "💖",
        "buff": "🛡️",
        "system": "⚙️"
    }

    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def __getattr__(self, name: str):
        if name in self.SYMBOLS:
            return lambda msg, **kwargs: self._log(name, msg, **kwargs)
        raise AttributeError(f"'CombatLogger' object has no attribute '{name}'")

    def _log(self, event_type: str, message: str, **kwargs: Any):
        symbol = self.SYMBOLS.get(event_type, "📝")
        bar_str = ""
        if "val" in kwargs and "max_val" in kwargs:
            val = max(0, min(kwargs["val"], kwargs["max_val"]))
            max_val = kwargs["max_val"]
            filled = int((val / max_val) * 10) if max_val > 0 else 0
            bar_str = f" [{'#' * filled}{'-' * (10 - filled)}] ({val}/{max_val})"

        target = f" -> [{kwargs['target']}]" if "target" in kwargs else ""
        log_line = f"[{symbol} {event_type.upper()}]{target} {message}{bar_str}\n"
        self.stream.write(log_line)
        self.stream.flush()