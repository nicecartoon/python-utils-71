import enum

class GameErrorCodes(enum.IntEnum):
    SUCCESS = 0
    PLAYER_DISCONNECTED = 4001
    INVALID_STATE_TRANSITION = 4002
    ASSET_LOAD_FAILURE = 4003
    MEMORY_BUFFER_OVERFLOW = 4004
    UNRECOVERABLE_GPU_CRASH = 5000

ERROR_MESSAGES = {
    GameErrorCodes.PLAYER_DISCONNECTED: "Player connection heartbeat lost during sync.",
    GameErrorCodes.INVALID_STATE_TRANSITION: "Illegal state switch requested by client.",
    GameErrorCodes.ASSET_LOAD_FAILURE: "Requested texture or mesh missing from registry.",
    GameErrorCodes.MEMORY_BUFFER_OVERFLOW: "Heap exhaustion in rendering pipe.",
    GameErrorCodes.UNRECOVERABLE_GPU_CRASH: "Fatal hardware abstraction layer violation."
}

def get_error_context(code: int) -> dict:
    """Fetches error metadata with fallback for unknown codes."""
    base_info = {
        "code": code,
        "msg": ERROR_MESSAGES.get(code, "Unknown engine anomaly detected."),
        "severity": "critical" if code >= 5000 else "warning"
    }
    return base_info

RETRY_LIMIT = 3
FATAL_EXIT_CODES = [GameErrorCodes.UNRECOVERABLE_GPU_CRASH, GameErrorCodes.MEMORY_BUFFER_OVERFLOW]