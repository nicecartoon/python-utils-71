import functools
import time

class EntityCache:
    def __init__(self, capacity=128):
        self.capacity = capacity
        self.storage = {}
        self.order = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in self.storage:
                self.order.remove(key)
                self.order.append(key)
                return self.storage[key]
            
            result = func(*args, **kwargs)
            if len(self.storage) >= self.capacity:
                oldest = self.order.pop(0)
                del self.storage[oldest]
            
            self.storage[key] = result
            self.order.append(key)
            return result
        return wrapper

@EntityCache(capacity=256)
def calculate_hitbox_mesh(entity_id, scale_factor):
    # Simulated expensive geometry generation
    time.sleep(0.01)
    return f"mesh_data_{entity_id}_{scale_factor}"

def batch_process_entities(entities):
    return [calculate_hitbox_mesh(e, 1.0) for e in entities]

if __name__ == '__main__':
    data = list(range(100))
    start = time.perf_counter()
    batch_process_entities(data)
    batch_process_entities(data)
    print(f"optimized mesh generation in {time.perf_counter() - start:.4f}s")