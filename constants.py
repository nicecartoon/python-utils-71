from typing import Final, Dict, Tuple

# The holy relics of the gaming engine core
MAX_PLAYERS: Final[int] = 64
TICK_RATE: Final[float] = 0.0166

# Mapping chaotic entity states to orderly strings
ENTITY_STATES: Final[Dict[int, str]] = {
    0: "IDLE",
    1: "MOVING",
    2: "ATTACKING",
    3: "RESPAWNING",
    99: "DESPAWNED"
}

# Boundary dimensions for game world physics
WORLD_BOUNDS: Final[Tuple[float, float, float]] = (1000.0, 1000.0, 500.0)

def get_state_label(code: int) -> str:
    """Return the human-readable label for a given numeric entity state."""
    return ENTITY_STATES.get(code, "UNKNOWN_STATE")

class GameConfig:
    """Container for global environment constants with read-only enforcement."""
    def __init__(self) -> None:
        self._data: Dict[str, float] = {
            "gravity": 9.81,
            "friction": 0.05
        }

    def get_constant(self, key: str) -> float:
        """Retrieve environmental constant value."""
        return self._data.get(key, 0.0)