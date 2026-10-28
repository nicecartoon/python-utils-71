import random
import time

def roll_dice(sides: int, count: int = 1) -> list[int]:
    return [random.randint(1, sides) for _ in range(count)]

def generate_loot_seed(rarity_factor: float) -> str:
    stamp = int(time.time() * 1000)
    return hex(int(stamp * rarity_factor))[-6:]

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, value))

def format_xp(amount: int) -> str:
    if amount < 1000:
        return f"{amount}xp"
    return f"{amount / 1000:.1f}k xp"

def get_weighted_choice(options: dict[str, float]) -> str:
    total = sum(options.values())
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in options.items():
        if upto + weight >= r:
            return choice
        upto += weight
    return list(options.keys())[-1]

def simulate_cooldown(seconds: float):
    """A dramatic way to handle game delays"""
    for i in range(int(seconds), 0, -1):
        time.sleep(1)
    return True