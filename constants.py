from typing import Final, Dict, Tuple

# Gaming mechanics configurations for python-utils-71

MAX_PLAYERS: Final[int] = 64
DEFAULT_TICK_RATE: Final[float] = 0.0166667

LEVEL_MODIFIERS: Final[Dict[str, float]] = {
    "easy": 0.8,
    "normal": 1.0,
    "hard": 1.5,
    "insane": 2.5
}

COORDINATE_BOUNDS: Final[Tuple[int, int, int, int]] = (0, 0, 1024, 1024)

class GameConstants:
    """
    Namespace for static game-engine properties.
    Implements a locked-value pattern for consistent state.
    """
    def __init__(self) -> None:
        self._data: Dict[str, any] = {
            "GRAVITY": 9.81,
            "FRICTION": 0.05
        }

    def get(self, key: str) -> float:
        """
        Retrieves physics constant with fallback.
        """
        return float(self._data.get(key, 0.0))

# Instantiate singleton for global access
physics_engine_defaults: Final[GameConstants] = GameConstants()