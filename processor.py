import functools
import random
import time

def retry_on_failure(retries=3, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retries - 1: raise
                    time.sleep(delay * (2 ** i))
            return None
        return wrapper
    return decorator

def calculate_loot_drop(item_pool, luck_modifier=1.0):
    weights = [item['rarity'] * luck_modifier for item in item_pool]
    return random.choices(item_pool, weights=weights, k=1)[0]

def normalize_coordinates(x, y, max_bounds=(1024, 768)):
    return (max(0, min(x, max_bounds[0])), max(0, min(y, max_bounds[1])))

def session_id_generator(prefix='G'):
    timestamp = hex(int(time.time()))[2:]
    random_hex = hex(random.getrandbits(16))[2:]
    return f"{prefix}-{timestamp}-{random_hex}".upper()

def batch_process_entities(entities, action_func, batch_size=10):
    results = []
    for i in range(0, len(entities), batch_size):
        batch = entities[i:i + batch_size]
        results.extend([action_func(e) for e in batch])
    return results