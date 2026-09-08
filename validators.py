from typing import Any, Callable, Dict, Union

class Validator:
    """A composable game-stat validator utilizing bitwise operators for rule construction."""

    def __init__(self, func: Callable[[Any], bool], error_msg: str) -> None:
        self.func = func
        self.error_msg = error_msg

    def __call__(self, value: Any) -> bool:
        """Evaluate the validator function against the provided game value."""
        return self.func(value)

    def __and__(self, other: "Validator") -> "Validator":
        """Chain validators with the bitwise AND (&) operator for strict multi-rule evaluation."""
        return Validator(
            lambda v: self(v) and other(v),
            f"({self.error_msg} AND {other.error_msg})"
        )

    def __or__(self, other: "Validator") -> "Validator":
        """Chain validators with the bitwise OR (|) operator for alternative validation rules."""
        return Validator(
            lambda v: self(v) or other(v),
            f"({self.error_msg} OR {other.error_msg})"
        )

# Concrete validator instances for game attributes
is_non_negative = Validator(lambda x: isinstance(x, (int, float)) and x >= 0, "must be a non-negative number")
is_string = Validator(lambda x: isinstance(x, str), "must be a text string")
is_rarity = Validator(lambda x: x in {"common", "rare", "epic", "legendary"}, "must be a valid rarity tier")

def validate_game_entity(entity: Dict[str, Any], schema: Dict[str, Validator]) -> bool:
    """Validates a game entity dictionary against a schema of combined validator rules.

    Raises ValueError if any rule is breached, detailing the offending schema violation.
    """
    for key, validator in schema.items():
        if key not in entity:
            raise ValueError(f"Missing required game attribute: '{key}'")
        if not validator(entity[key]):
            raise ValueError(f"Invalid game attribute '{key}': {validator.error_msg} (got value: {entity[key]!r})")
    return True