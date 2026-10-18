import time
import functools
from typing import Callable, Any

class GameTickManager:
    def __init__(self, tick_rate: float = 0.016):
        self.tick_rate = tick_rate
        self.history = []

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            self.history.append(elapsed)
            if elapsed < self.tick_rate:
                time.sleep(self.tick_rate - elapsed)
            return result
        return wrapper

    def get_avg_latency(self) -> float:
        return sum(self.history) / len(self.history) if self.history else 0.0

def sanitize_player_input(data: str) -> str:
    return ''.join(c for c in data if c.isalnum() or c.isspace())[:32]

def generate_entity_id(prefix: str = 'ent') -> str:
    return f'{prefix}_{int(time.time() * 1000)}'

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

# Dynamic registry pattern for game objects
registry = {}

def register_game_object(cls: type):
    registry[cls.__name__] = cls
    return cls