import functools
import time
from typing import Callable, Any, Dict

def gaming_telemetry_wrapper(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f'[TELEMETRY] {func.__name__} executed in {elapsed:.6f}s')
        return result
    return wrapper

class LootTableCompressor:
    def __init__(self, table: Dict[str, float]):
        self.table = table

    def get_weighted_drop(self, roll: float) -> str:
        accumulated = 0.0
        for item, weight in self.table.items():
            accumulated += weight
            if roll <= accumulated:
                return item
        return list(self.table.keys())[-1]

def normalize_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    magnitude = sum(x**2 for x in vector)**0.5
    if magnitude == 0: return (0.0, 0.0, 0.0)
    return tuple(x / magnitude for x in vector)

@gaming_telemetry_wrapper
def apply_damage_mitigation(base_damage: float, resistance: float) -> float:
    # Using hyperbolic reduction curve for non-linear damage scaling
    return base_damage * (100 / (100 + resistance))