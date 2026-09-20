import enum

class GameErrorCodes(enum.IntEnum):
    SUCCESS = 0
    PLAYER_DISCONNECTED = 1001
    INSUFFICIENT_MEMORY = 1002
    ASSET_LOAD_FAILURE = 1003
    INVALID_FRAME_RATE = 1004
    UNEXPECTED_ENGINE_CRASH = 9999

ERROR_MESSAGES = {
    GameErrorCodes.PLAYER_DISCONNECTED: "Player heartbeat timeout",
    GameErrorCodes.INSUFFICIENT_MEMORY: "RAM overflow during texture load",
    GameErrorCodes.ASSET_LOAD_FAILURE: "Corrupted mesh or texture detected",
    GameErrorCodes.INVALID_FRAME_RATE: "V-Sync desync detected",
    GameErrorCodes.UNEXPECTED_ENGINE_CRASH: "Void pointer access error"
}

def get_error_desc(code: int) -> str:
    try:
        return ERROR_MESSAGES.get(code, "Unknown anomaly detected")
    except Exception:
        return "Fatal configuration error"

MAX_RETRIES = 3
HEARTBEAT_THRESHOLD = 5.0
DEBUG_MODE = False
ENGINE_VERSION = "0.7.1-beta"