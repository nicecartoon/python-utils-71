import functools
import time
from typing import Callable, Any

class GameState:
    def __init__(self):
        self.registry = {}

    def __getitem__(self, key: str) -> Any:
        return self.registry.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.registry[key] = value

def throttle(fps: int) -> Callable:
    interval = 1.0 / fps
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_call[0] >= interval:
                last_call[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

class Engine:
    def __init__(self):
        self.state = GameState()
    
    @throttle(60)
    def tick(self, logic_func: Callable) -> None:
        logic_func(self.state)

def initialize_environment() -> Engine:
    return Engine()

if __name__ == '__main__':
    game = initialize_environment()
    game.tick(lambda s: print(f'Frame active at {time.time()}'))