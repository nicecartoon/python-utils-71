import time
import random
from functools import wraps

def gaming_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'[METRIC] {func.__name__} latency: {time.perf_counter() - start:.6f}s')
        return result
    return wrapper

def roll_dice(sides=6, count=1):
    return [random.randint(1, sides) for _ in range(count)]

def clamp(value, low, high):
    return max(low, min(value, high))

def chunk_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]

def lerp_color(c1, c2, t):
    t = clamp(t, 0.0, 1.0)
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def format_inventory(items):
    return ' | '.join([f'[{i.upper()}]' for i in items])

class EntityPool:
    def __init__(self, capacity=100):
        self.pool = [None] * capacity
        
    def spawn(self, entity):
        for i, slot in enumerate(self.pool):
            if slot is None:
                self.pool[i] = entity
                return i
        return -1