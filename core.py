import functools
import time

class EntityCache:
    def __init__(self):
        self._storage = {}
        self._hits = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in self._storage:
                self._storage[key] = func(*args, **kwargs)
            else:
                self._hits += 1
            return self._storage[key]
        return wrapper

    def purge(self):
        self._storage.clear()

cache = EntityCache()

@cache
def calculate_physics_frame(entity_id: int, delta: float) -> dict:
    time.sleep(0.01)
    return {"id": entity_id, "pos": delta * 1.05, "status": "active"}

def process_game_state(entities: list, dt: float):
    results = []
    for eid in entities:
        results.append(calculate_physics_frame(eid, dt))
    return results

if __name__ == '__main__':
    entities = [101, 102, 103]
    print(process_game_state(entities, 0.016))