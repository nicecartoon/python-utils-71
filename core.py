import time
import random
from typing import Callable, Any

def loot_generator(rarity: str) -> dict:
    loot_table = {'common': 0.8, 'rare': 0.15, 'legendary': 0.05}
    roll = random.random()
    item = 'wood' if roll < loot_table.get(rarity, 0.5) else 'sword'
    return {'item': item, 'timestamp': time.time()}

def throttle(rate_limit: float) -> Callable:
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < rate_limit:
                time.sleep(rate_limit - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@throttle(0.1)
def spawn_entity(name: str) -> str:
    return f'entity {name} spawned at {time.time()}'

def validate_player_state(hp: int, mana: int) -> bool:
    return all([isinstance(hp, int), isinstance(mana, int), hp >= 0, mana >= 0])

def batch_process(items: list, action: Callable) -> list:
    return [action(i) for i in items]