import math
from typing import Any, List, Dict, Callable

class GameProcessor:
    def __init__(self, multiplier: float = 1.0):
        self.multiplier = multiplier

    def apply_damage(self, health: int, damage: int) -> int:
        return max(0, health - int(damage * self.multiplier))

    def interpolate(self, start: float, end: float, alpha: float) -> float:
        return start + (end - start) * max(0.0, min(1.0, alpha))

    def batch_process(self, data: List[Any], func: Callable) -> List[Any]:
        return [func(item) for item in data]

    def calculate_cooldown(self, base: float, level: int) -> float:
        return base * (0.9 ** (level - 1))

    def normalize_vector(self, x: float, y: float) -> tuple:
        mag = math.sqrt(x**2 + y**2)
        return (x / mag, y / mag) if mag > 0 else (0.0, 0.0)

    def pack_game_state(self, entity_map: Dict[str, Any]) -> str:
        return '|'.join([f"{k}:{v}" for k, v in entity_map.items()])

    def unpack_game_state(self, packet: str) -> Dict[str, str]:
        return dict(item.split(':') for item in packet.split('|'))