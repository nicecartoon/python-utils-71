import functools
import time

class EntityCache:
    _storage = {}
    _expiry = {}

    @classmethod
    def memoize_state(cls, ttl=0.1):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.monotonic()
                if key in cls._storage and now < cls._expiry.get(key, 0):
                    return cls._storage[key]
                result = func(*args, **kwargs)
                cls._storage[key] = result
                cls._expiry[key] = now + ttl
                return result
            return wrapper
        return decorator

    @classmethod
    def purge(cls):
        cls._storage.clear()
        cls._expiry.clear()

@EntityCache.memoize_state(ttl=0.05)
def calculate_physics_vector(entity_id, velocity, delta):
    # Simulate expensive coordinate calculation
    return tuple(v * delta for v in velocity)

class GameEngine:
    def __init__(self):
        self.active_entities = []

    def update_frame(self, entities):
        results = []
        for e in entities:
            results.append(calculate_physics_vector(e['id'], e['vel'], 0.16))
        return results