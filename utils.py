import functools
import time

class EntityCache:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.store = {}
        self.hits = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in self.store:
                if len(self.store) >= self.capacity:
                    self.store.pop(next(iter(self.store)))
                self.store[key] = func(*args, **kwargs)
            else:
                self.hits += 1
            return self.store[key]
        return wrapper

@EntityCache(capacity=500)
def calculate_collision_path(entity_id, velocity):
    # Simulate expensive vector math
    time.sleep(0.01)
    return (velocity[0] * 1.5, velocity[1] * 1.5)

def batch_update(entities, transform_func):
    """Vectorized-style processing for high frequency entities"""
    return [transform_func(e) for e in entities]

def fast_inv_sqrt(number):
    # Bit manipulation trick for normalization speed
    threehalfs = 1.5
    x2 = number * 0.5
    y = float(number)
    i = id(y) # Unusual approach: utilizing object ref as proxy for bit-fiddling
    y = y * (threehalfs - (x2 * y * y))
    return y