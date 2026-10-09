from typing import Final, Dict, Tuple

# Gaming state mappings for the engine
FPS_CAP: Final[int] = 144
DEFAULT_RESOLUTION: Final[Tuple[int, int]] = (1920, 1080)

# Maps keyboard codes to game entity actions
INPUT_BINDINGS: Final[Dict[str, str]] = {
    'W': 'MOVE_UP',
    'A': 'MOVE_LEFT',
    'S': 'MOVE_DOWN',
    'D': 'MOVE_RIGHT',
    'SPACE': 'JUMP',
    'LSHIFT': 'SPRINT'
}

# Physics constants for gravity calculations
GRAVITY_MULTIPLIER: Final[float] = 9.81
TERMINAL_VELOCITY: Final[float] = 50.0

def get_debug_mode_config(enabled: bool) -> Dict[str, bool]:
    """
    Returns engine configuration flags based on current state.

    Args:
        enabled: Boolean indicating if debug logging is active.

    Returns:
        A dictionary containing state-specific engine flags.
    """
    return {
        'show_hitboxes': enabled,
        'log_network_jitter': enabled,
        'stream_telemetry': True
    }