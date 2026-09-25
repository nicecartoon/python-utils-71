import time
import random
from typing import Any, Callable

def jittered_backoff(retries: int = 3, base_delay: float = 0.1):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == retries - 1: raise
                    sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def loot_generator(pool: dict[str, float]) -> str:
    r = random.random()
    accumulator = 0.0
    for item, chance in pool.items():
        accumulator += chance
        if r <= accumulator:
            return item
    return list(pool.keys())[-1]

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def format_ticks(ticks: int) -> str:
    seconds = ticks // 60
    return f"{seconds // 60:02}:{seconds % 60:02}:{ticks % 60:02}"