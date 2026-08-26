import time
from functools import lru_cache

class GameStateOptimizer:
    def __init__(self, capacity: int = 1024):
        self.capacity = capacity
        self._tick_history = []

    @lru_cache(maxsize=128)
    def calculate_trajectory(self, velocity: float, angle: float, gravity: float = 9.81) -> float:
        import math
        rad = math.radians(angle)
        return (pow(velocity, 2) * math.sin(2 * rad)) / gravity

    def batch_process_entities(self, entities: list, delta_time: float) -> list:
        optimized_updates = []
        for entity in entities:
            pos = entity.get('position', (0.0, 0.0))
            vel = entity.get('velocity', (0.0, 0.0))
            new_pos = (
                pos[0] + vel[0] * delta_time,
                pos[1] + vel[1] * delta_time
            }
            optimized_updates.append({'id': entity['id'], 'position': new_pos})
        return optimized_updates

    def profile_execution(self, func, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        self._tick_history.append(duration)
        if len(self._tick_history) > self.capacity:
            self._tick_history.pop(0)
        return result

    def get_average_tick_time(self) -> float:
        if not self._tick_history:
            return 0.0
        return sum(self._tick_history) / len(self._tick_history)
