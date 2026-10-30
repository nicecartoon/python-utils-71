import random
import time

def roll_dice(sides: int = 6, count: int = 1) -> list:
    return [random.randint(1, sides) for _ in range(count)]

def calculate_dps(damage: float, duration: float) -> float:
    return damage / duration if duration > 0 else 0.0

def throttle_action(interval: float):
    last_called = 0.0
    def decorator(func):
        nonlocal last_called
        def wrapper(*args, **kwargs):
            nonlocal last_called
            now = time.time()
            if now - last_called >= interval:
                last_called = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

def paginate_inventory(items: list, size: int) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]

def format_xp(xp: int) -> str:
    if xp >= 1_000_000:
        return f'{xp / 1_000_000:.2f}M XP'
    if xp >= 1_000:
        return f'{xp / 1_000:.1f}K XP'
    return f'{xp} XP'

class StatsCache:
    def __init__(self):
        self._data = {}
    def update(self, key: str, val: any):
        self._data[key] = {'v': val, 't': time.time()}
    def get(self, key: str, expiry: float):
        entry = self._data.get(key)
        if entry and (time.time() - entry['t'] < expiry):
            return entry['v']
        return None