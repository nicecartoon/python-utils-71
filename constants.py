import enum
import math
from typing import Final

class GameTick(float, enum.Enum):
    UI_UPDATE = 0.016
    PHYSICS_STEP = 0.033
    NETWORK_SYNC = 0.1

class EntityState(str, enum.Enum):
    SPAWNED = 'spawned'
    ACTIVE = 'active'
    STUNNED = 'stunned'
    DELETED = 'deleted'

MAX_PLAYERS: Final[int] = 64
GRAVITY_CONSTANT: Final[float] = -9.81

def calculate_bounding_box(size: float, padding: float = 1.0) -> tuple[float, float]:
    """Calculates dimensions for grid-based collision detection."""
    dimension = math.ceil(size * padding)
    return (dimension, dimension)

def format_tick_rate(tick: GameTick) -> str:
    """Converts float tick rate to a human-readable identifier."""
    return f"TICK_RATE_{int(1/tick)}"

ERROR_CODES: Final[dict[int, str]] = {
    4001: 'PLAYER_DISCONNECTED',
    4002: 'PACKET_LOSS_CRITICAL',
    4003: 'ENTITY_OOB'
}

PLAYER_COLORS: Final[list[str]] = ['#FF5733', '#33FF57', '#3357FF', '#F333FF']