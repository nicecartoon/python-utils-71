import functools
import time

class CacheNode:
    def __init__(self, ttl=5.0):
        self.ttl = ttl
        self.data = {}
        self.expiry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.data and now < self.expiry.get(key, 0):
                return self.data[key]
            result = func(*args, **kwargs)
            self.data[key] = result
            self.expiry[key] = now + self.ttl
            return result
        return wrapper

memoize_frame = CacheNode(ttl=0.1)

@memoize_frame
def calculate_collision(entity_a, entity_b):
    # Simulate expensive geometric calculation
    dx = entity_a.x - entity_b.x
    dy = entity_a.y - entity_b.y
    return (dx**2 + dy**2)**0.5 < 10.0

def batch_process(entities, processor_func):
    return [processor_func(e) for e in entities]

def optimized_range_check(center, radius, entities):
    return [e for e in entities if (e.x - center[0])**2 + (e.y - center[1])**2 <= radius**2]