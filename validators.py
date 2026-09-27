"""Validation utilities for player stats, inventories, and spatial game coordinates."""

from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T")
ValidationResult = Tuple[bool, Optional[str]]


class GamingRule:
    """Combinator for gaming validation rules supporting bitwise OR logic."""

    def __init__(self, check: Callable[[Any], bool], error_msg: str) -> None:
        """Initialize rule with a condition check function and failure message."""
        self.check = check
        self.error_msg = error_msg

    def __call__(self, value: Any) -> ValidationResult:
        """Validate value against rule condition."""
        return (True, None) if self.check(value) else (False, self.error_msg)

    def __or__(self, other: "GamingRule") -> "GamingRule":
        """Combine two gaming rules with logical OR operator fallback."""
        return GamingRule(
            lambda val: self.check(val) or other.check(val),
            f"Failed both: [{self.error_msg}] OR [{other.error_msg}]",
        )


def validate_player_speed(speed: float, max_allowed: float = 250.0) -> ValidationResult:
    """Check if player move speed is non-negative and within server anti-cheat limits."""
    type_rule = GamingRule(lambda s: isinstance(s, (int, float)), "Speed must be numeric")
    bound_rule = GamingRule(lambda s: 0.0 <= float(s) <= max_allowed, f"Speed out of bounds (0-{max_allowed})")

    ok, err = type_rule(speed)
    return (ok, err) if not ok else bound_rule(speed)


def validate_inventory_grid(items: List[Dict[str, Any]], max_slots: int = 20) -> ValidationResult:
    """Verify inventory item count and matrix positioning without cell overlap."""
    if len(items) > max_slots:
        return False, f"Inventory capacity exceeded: {len(items)}/{max_slots}"

    occupied: set[Tuple[int, int]] = set()
    for item in items:
        x, y = item.get("x", -1), item.get("y", -1)
        w, h = item.get("w", 1), item.get("h", 1)
        if x < 0 or y < 0:
            return False, f"Invalid grid position for item '{item.get('id', 'unknown')}'"
        for dx in range(w):
            for dy in range(h):
                coord = (x + dx, y + dy)
                if coord in occupied:
                    return False, f"Grid collision detected at coordinate {coord}"
                occupied.add(coord)
    return True, None


def validate_guild_tag(tag: str) -> ValidationResult:
    """Ensure guild tag follows tournament standard [A-Z0-9] format and length."""
    valid_len = GamingRule(lambda t: isinstance(t, str) and 2 <= len(t) <= 5, "Tag length must be 2-5 chars")
    valid_chars = GamingRule(lambda t: str(t).isalnum() and str(t).isupper(), "Tag must be uppercase alphanumeric")

    for rule in (valid_len, valid_chars):
        ok, err = rule(tag)
        if not ok:
            return ok, err
    return True, None