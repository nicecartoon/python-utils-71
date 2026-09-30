from typing import List, Union, Callable, Any

GameScore = Union[int, float]

def calculate_experience_multiplier(level: int, base: float = 1.0) -> float:
    """Calculates exponential experience gain based on player level."""
    return base * (1.1 ** (level - 1))

def apply_buffs(stats: List[int], modifier: Callable[[int], int]) -> List[int]:
    """Applies a functional transformation to a list of player stats."""
    return [modifier(s) for s in stats]

class EntityFactory:
    """Generator for spawning game entities with unique identifiers."""
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self._counter = 0

    def spawn(self, entity_type: str) -> str:
        """Creates a unique entity tag string."""
        self._counter += 1
        return f"{self.prefix}_{entity_type}_{self._counter:03d}"

def normalize_coordinates(coords: tuple[float, float]) -> tuple[int, int]:
    """Maps float game space coordinates to discrete integer grid slots."""
    x, y = coords
    return int(round(x)), int(round(y))

def process_inventory(items: List[Any], filter_func: Callable[[Any], bool]) -> List[Any]:
    """Filters inventory lists using a custom condition predicate."""
    return [item for item in items if filter_func(item)]