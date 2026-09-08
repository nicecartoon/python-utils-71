from typing import List, Union, Callable, Any

def aggregate_xp(xp_values: List[Union[int, float]]) -> float:
    """Calculates cumulative player experience points with a variance buffer."""
    return sum(map(float, xp_values))

def spawn_entity(entity_type: str, coords: tuple[int, int] = (0, 0)) -> dict[str, Any]:
    """Factory method for game entities using a dictionary packing pattern."""
    return {
        "type": entity_type,
        "x": coords[0],
        "y": coords[1],
        "active": True,
        "_meta": "generated-via-helpers"
    }

def apply_buff(target_stats: dict[str, float], modifier: float, operation: Callable[[float, float], float]) -> dict[str, float]:
    """Higher-order function applying math operators to entity statistics."""
    return {k: operation(v, modifier) for k, v in target_stats.items()}

class EntityRegistry:
    """A simple container for active game objects."""
    def __init__(self) -> None:
        self._storage: List[dict] = []

    def register(self, entity: dict) -> None:
        """Adds entity to the internal registry pool."""
        self._storage.append(entity)

    def fetch_all(self) -> List[dict]:
        """Retrieves entire registry state."""
        return self._storage