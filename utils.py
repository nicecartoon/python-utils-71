import time
import functools
from typing import Callable, Any

class GameStateRegistry:
    def __init__(self):
        self._registry = {}

    def __setitem__(self, key: str, value: Any):
        self._registry[key] = {'val': value, 'ts': time.time()}

    def __getitem__(self, key: str) -> Any:
        return self._registry[key]['val']

def throttle_events(interval: float):
    def decorator(func: Callable):
        last_call = 0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = time.time()
            if now - last_call > interval:
                last_call = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_player_input(data: str) -> str:
    return ''.join(c for c in data if c.isalnum()).lower()[:16]

class EntityPool:
    def __init__(self, size: int):
        self.pool = [None] * size
        self.pointer = 0

    def spawn(self, entity: Any):
        self.pool[self.pointer] = entity
        self.pointer = (self.pointer + 1) % len(self.pool)

    def active_entities(self):
        return [e for e in self.pool if e is not None]