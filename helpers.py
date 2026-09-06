from typing import List, Union, Callable, Any

def aggregate_xp(levels: List[int], multiplier: float = 1.0) -> int:
    """Calculates total experience points from a list of player levels."""
    return int(sum(level * 100 for level in levels) * multiplier)

def sanitize_player_name(name: str) -> str:
    """Removes non-alphanumeric characters for gaming leaderboard display."""
    return ''.join(char for char in name if char.isalnum())

def apply_buff(stat: float, modifier: Union[int, float], op: Callable[[float, float], float] = lambda a, b: a + b) -> float:
    """Applies a mathematical operation to a stat value.
    
    Default operation is addition of the modifier.
    """
    return float(op(stat, float(modifier)))

class EntityMapper:
    """Maps raw gaming entities to internal object representation."""
    def __init__(self, entities: List[Any]) -> None:
        self.data = {str(i): e for i, e in enumerate(entities)}

    def get_count(self) -> int:
        """Returns total count of registered entities."""
        return len(self.data)