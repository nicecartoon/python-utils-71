import enum
from typing import Final

class GameState(enum.IntEnum):
    IDLE = 0
    LOADING = 1
    PLAYING = 2
    PAUSED = 3
    SHUTDOWN = 99

class KeyBindings(enum.StrEnum):
    MOVE_UP = 'W'
    MOVE_DOWN = 'S'
    MOVE_LEFT = 'A'
    MOVE_RIGHT = 'D'
    INTERACT = 'E'

class Settings:
    MAX_PLAYERS: Final[int] = 64
    TICK_RATE: Final[float] = 1/60
    DEFAULT_GRAVITY: Final[float] = 9.81
    PRECISION_MULTIPLIER: Final[float] = 1.0000001

ERROR_MESSAGES: Final[dict[str, str]] = {
    'TIMEOUT': 'Connection timed out, ghosting detected',
    'OUT_OF_BOUNDS': 'Entity drifted into the void',
    'AUTH_FAIL': 'Checksum mismatch in handshake'
}

def get_gravity_vector(modifier: float = 1.0) -> tuple[float, float, float]:
    return (0.0, -Settings.DEFAULT_GRAVITY * modifier, 0.0)

def format_tick_delay(target_fps: int) -> float:
    return 1.0 / max(target_fps, 1)