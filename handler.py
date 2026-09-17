import functools
import time

class EntityCache:
    _storage = {}
    _expiry = {}
    
    @classmethod
    def get_optimized_state(cls, entity_id, ttl=0.1):
        now = time.time()
        if entity_id in cls._storage and now < cls._expiry.get(entity_id, 0):
            return cls._storage[entity_id]
        return None

    @classmethod
    def update(cls, entity_id, data, ttl=0.1):
        cls._storage[entity_id] = data
        cls._expiry[entity_id] = time.time() + ttl

def fast_process(func):
    @functools.wraps(func)
    def wrapper(entity_id, *args, **kwargs):
        cached = EntityCache.get_optimized_state(entity_id)
        if cached is not None:
            return cached
        result = func(entity_id, *args, **kwargs)
        EntityCache.update(entity_id, result)
        return result
    return wrapper

@fast_process
def calculate_entity_path(entity_id):
    # Simulate expensive game engine pathfinding
    time.sleep(0.05)
    return f"path_data_{entity_id}_{hash(str(time.time()))}"