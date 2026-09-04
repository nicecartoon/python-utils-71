import functools
from typing import Callable, Any

def gaming_pipeline(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[!] engine crash in {func.__name__}: {e}")
            return None
    return wrapper

class EntityProcessor:
    def __init__(self, entities: list) -> None:
        self._registry = {e['id']: e for e in entities}

    @gaming_pipeline
    def update_stats(self, entity_id: str, delta: dict) -> None:
        target = self._registry.get(entity_id)
        if target:
            for key, val in delta.items():
                target[key] = target.get(key, 0) + val

    def get_active_entities(self) -> list:
        return sorted(
            self._registry.values(), 
            key=lambda x: x.get('power', 0), 
            reverse=True
        )

    def flush_registry(self) -> None:
        self._registry = {}

if __name__ == "__main__":
    proc = EntityProcessor([{'id': 'player1', 'power': 10}])
    proc.update_stats('player1', {'power': 5})
    print(proc.get_active_entities())