import functools
import time
import random
from typing import Callable, Any

def jitter_retry(retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(base_delay * (2 ** i) + random.uniform(0, 0.1))
            raise last_ex
        return wrapper
    return decorator

def loot_table_roll(items: dict[str, float]) -> str:
    r = random.random()
    cumulative = 0.0
    for item, weight in items.items():
        cumulative += weight
        if r <= cumulative:
            return item
    return list(items.keys())[-1]

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

class GameTimer:
    def __init__(self):
        self.start_time = time.perf_counter()

    def tick(self) -> float:
        now = time.perf_counter()
        delta = now - self.start_time
        self.start_time = now
        return delta