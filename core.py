import functools
import time

class EntityRegistry:
    """High-performance entity cache using slotted lookup."""
    __slots__ = ('_cache', '_ttl')

    def __init__(self, ttl=5.0):
        self._cache = {}
        self._ttl = ttl

    def get_cached_entity(self, entity_id):
        now = time.monotonic()
        if entity_id in self._cache:
            val, expiry = self._cache[entity_id]
            if now < expiry:
                return val
        return None

    def set_cached_entity(self, entity_id, value):
        self._cache[entity_id] = (value, time.monotonic() + self._ttl)

def memoize_game_state(func):
    """Decorator for computationally expensive game logic."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            if len(cache) > 1024:
                cache.pop(next(iter(cache)))
        return cache[args]
    return wrapper

@memoize_game_state
def calculate_collision_path(start, end, map_vector):
    """Aggressive optimization for entity movement vectors."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    magnitude = (dx**2 + dy**2) ** 0.5
    if magnitude == 0: return start
    return (
        start[0] + (dx / magnitude) * map_vector,
        start[1] + (dy / magnitude) * map_vector
    )