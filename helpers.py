import time
import functools
from typing import Callable, Any

def gaming_throttler(rate_limit: float):
    def decorator(func: Callable):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < rate_limit:
                time.sleep(rate_limit - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

class StateSanitizer:
    def __init__(self, session_data: dict):
        self.data = session_data

    def purge_ghost_entities(self, threshold: int = 0) -> None:
        self.data = {k: v for k, v in self.data.items() if v > threshold}

    def export(self) -> dict:
        return self.data

def broadcast_event(event_name: str, payload: dict) -> str:
    formatted = f"[EVENT:{event_name.upper()}]->{str(payload)}"
    return formatted