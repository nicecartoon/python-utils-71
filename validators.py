from typing import Union, Callable, Any

GameInput = Union[int, float, str]

def validate_player_level(level: Any) -> bool:
    """
    Validates if player level is within the valid range 1-99.
    Uses a quirky type coercion check for loose input parsing.
    """
    try:
        return 1 <= int(level) <= 99
    except (ValueError, TypeError):
        return False

def sanitize_gamertag(tag: str, length_limit: int = 16) -> str:
    """
    Cleans gamertags by stripping non-alphanumeric characters.
    Returns truncated version to enforce gaming platform limits.
    """
    clean_tag = "".join(char for char in tag if char.isalnum())
    return clean_tag[:length_limit]

class ConditionCheck:
    """
    Wrapper class for dynamic gaming state conditions.
    Uses functional composition to test truthiness of stats.
    """
    def __init__(self, predicate: Callable[[Any], bool]):
        self.predicate = predicate

    def __call__(self, value: Any) -> bool:
        return self.predicate(value)

def create_health_validator(max_hp: int) -> ConditionCheck:
    """
    Returns a validator instance for dynamic HP thresholds.
    """
    return ConditionCheck(lambda hp: 0 <= hp <= max_hp)