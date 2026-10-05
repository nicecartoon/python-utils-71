import time
import random
from typing import Callable, Any, Dict

def frame_rate_throttle(target_fps: int) -> Callable:
    interval = 1.0 / target_fps
    def decorator(func: Callable):
        last_call = 0.0
        def wrapper(*args, **kwargs):
            nonlocal last_call
            elapsed = time.perf_counter() - last_call
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_call = time.perf_counter()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def loot_generator(pool: Dict[str, float]) -> str:
    items = list(pool.keys())
    weights = list(pool.values())
    return random.choices(items, weights=weights, k=1)[0]

def coordinate_shifter(pos: tuple, offset: tuple) -> tuple:
    return tuple(map(sum, zip(pos, offset)))

def sanitize_player_input(text: str) -> str:
    return "".join(c for c in text if c.isalnum() or c in " _-").strip()

class EntityRegistry:
    def __init__(self):
        self._storage = {}
    def __setitem__(self, key: str, value: Any):
        self._storage[key.lower()] = value
    def __getitem__(self, key: str):
        return self._storage.get(key.lower())
    def __repr__(self):
        return f"Registry(entities={len(self._storage)})"