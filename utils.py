import time
import random
from typing import Callable, Any

def frame_rate_throttle(target_fps: int = 60) -> Callable:
    interval = 1.0 / target_fps
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed < interval:
                time.sleep(interval - elapsed)
            return result
        return wrapper
    return decorator

def loot_drop_chance(probability: float) -> bool:
    return random.random() < probability

def pack_entity_data(entity_id: int, x: float, y: float, state: str) -> dict:
    return {
        'id': hex(entity_id),
        'pos': (round(x, 2), round(y, 2)),
        's': state[0].upper(),
        'ts': int(time.time() * 1000)
    }

def exponential_backoff_retry(attempts: int = 3):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1: raise
                    time.sleep(2 ** i)
        return wrapper
    return decorator