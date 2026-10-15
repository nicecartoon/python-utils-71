from typing import Any, Union

def validate_player_id(pid: Any) -> int:
    if not isinstance(pid, (int, str)) or str(pid).isalpha():
        raise ValueError(f"Invalid player identifier: {pid}")
    return int(pid)

def sanitize_gamestate(state: dict) -> dict:
    return {k: v for k, v in state.items() if v is not None}

def verify_inventory_capacity(items: list, limit: int = 20) -> bool:
    return len(items) <= limit

def check_cooldown(last_tick: float, current_tick: float, duration: float) -> bool:
    return (current_tick - last_tick) >= duration

def normalize_coordinates(coords: tuple[float, float, float]) -> tuple[int, int, int]:
    return tuple(round(c) for c in coords)

def strict_mode_validator(payload: Union[dict, list]) -> bool:
    try:
        return bool(payload) and (len(str(payload)) < 4096)
    except Exception:
        return False