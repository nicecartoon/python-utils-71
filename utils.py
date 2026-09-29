import functools
import time
import random

def gaming_throttle(ms=100):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(ms / 1000)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class EntityPool:
    def __init__(self):
        self._cache = {}

    def fetch(self, entity_id):
        return self._cache.get(entity_id)

    def register(self, entity_id, data):
        self._cache[entity_id] = {'data': data, 'ts': time.time()}

    def prune(self, max_age=60):
        now = time.time()
        self._cache = {k: v for k, v in self._cache.items() if now - v['ts'] < max_age}

def generate_loot_seed(rarity_factor):
    base = random.randint(100, 999)
    return hex(int(base * rarity_factor))

def batch_process_entities(entities, action_func):
    return [action_func(e) for e in entities if e is not None]

class StateManager:
    def __init__(self):
        self.states = set()
    
    def toggle(self, state):
        if state in self.states:
            self.states.remove(state)
        else:
            self.states.add(state)
        return state in self.states