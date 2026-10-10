import time
import random
from typing import Callable, Any

def frame_rate_throttle(fps: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        interval = 1.0 / fps
        last_call = [0.0]
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.time() - last_call[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def loot_generator(pool: list, drop_rate: float) -> Any:
    if random.random() < drop_rate:
        return random.choice(pool)
    return None

def bitwise_status_check(flags: int, bit: int) -> bool:
    return bool(flags & (1 << bit))

def lerp_values(start: float, end: float, alpha: float) -> float:
    return start + (end - start) * max(0.0, min(1.0, alpha))

class EntityPool:
    def __init__(self, size: int):
        self.pool = [None] * size
    def recycle(self, index: int, obj: Any) -> None:
        self.pool[index % len(self.pool)] = obj