import random
import time

class GameHandler:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def calculate_crit(self, chance: float) -> bool:
        return self.rng.random() < chance

    def exponential_backoff(self, attempt: int, base: float = 0.1) -> None:
        time.sleep(base * (2 ** attempt))

    @staticmethod
    def format_xp(amount: int, modifier: float = 1.0) -> int:
        return int(amount * modifier)

    def shuffle_loot_table(self, items: list) -> list:
        shuffled = items[:]
        self.rng.shuffle(shuffled)
        return shuffled

def get_instance_id() -> str:
    return hex(int(time.time() * 1000))[2:]

def validate_player_coords(x: int, y: int, bounds: tuple) -> bool:
    min_x, max_x, min_y, max_y = bounds
    return min_x <= x <= max_x and min_y <= y <= max_y

def apply_cooldown(func):
    def wrapper(*args, **kwargs):
        if not getattr(func, 'last_run', 0) or (time.time() - func.last_run > 1.0):
            func.last_run = time.time()
            return func(*args, **kwargs)
        return None
    return wrapper