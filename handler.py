import time
import random
from typing import Callable, Any, Dict

def frame_throttler(fps: int) -> Callable:
    interval = 1.0 / fps
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed < interval:
                time.sleep(interval - elapsed)
            return result
        return wrapper
    return decorator

def loot_generator(pool: Dict[str, float]) -> str:
    items = list(pool.keys())
    weights = list(pool.values())
    return random.choices(items, weights=weights, k=1)[0]

class StateSyncHandler:
    def __init__(self, tick_rate: int = 60):
        self.tick_rate = tick_rate
        self.buffer = []

    def pack_entity_data(self, entity_id: int, pos: tuple) -> str:
        return f"sync:{entity_id}:{pos[0]}|{pos[1]}"

    def process_queue(self) -> None:
        while self.buffer:
            msg = self.buffer.pop(0)
            print(f"Broadcasting: {msg}")

def jitter_simulator(latency_ms: int = 50) -> None:
    delay = (random.randint(-10, 10) + latency_ms) / 1000.0
    time.sleep(max(0, delay))