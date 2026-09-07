import time
import random
from typing import Any, Callable, Dict

class GameStateRegistry:
    _data: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, value: Any) -> None:
        cls._data[key] = value

    @classmethod
    def fetch(cls, key: str, default: Any = None) -> Any:
        return cls._data.get(key, default)

    @classmethod
    def purge(cls) -> None:
        cls._data.clear()

def retry_logic(attempts: int = 3):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(0.1 * (i + 1))
            raise last_ex
        return wrapper
    return decorator

@retry_logic(attempts=2)
def sync_player_score(player_id: str, score: int) -> bool:
    success = random.choice([True, False])
    if not success:
        raise ConnectionError("Server unreachable")
    GameStateRegistry.register(f"score_{player_id}", score)
    return True

def batch_process_entities(entities: list, processor: Callable) -> list:
    return [processor(e) for e in entities if e is not None]

class SessionManager:
    def __init__(self, session_id: str):
        self.sid = session_id
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        GameStateRegistry.purge()