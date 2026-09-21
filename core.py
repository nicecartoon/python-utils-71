import functools
import time

class GameTickOptimizer:
    def __init__(self, cache_size=128):
        self.cache_size = cache_size
        self._tick_cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self._tick_cache:
                return self._tick_cache[key]
            result = func(*args, **kwargs)
            if len(self._tick_cache) >= self.cache_size:
                self._tick_cache.pop(next(iter(self._tick_cache)))
            self._tick_cache[key] = result
            return result
        return wrapper

class CoreEngine:
    def __init__(self):
        self.optimization_engine = GameTickOptimizer()

    @staticmethod
    def compute_heavy_physics_frame(obj_id, vector_data):
        time.sleep(0.01)
        return sum(vector_data) * obj_id

    def execute_frame(self, obj_id, vector_data):
        cached_calc = self.optimization_engine(self.compute_heavy_physics_frame)
        return cached_calc(obj_id, tuple(vector_data))

engine = CoreEngine()
def update_physics(obj_id, data):
    return engine.execute_frame(obj_id, data)