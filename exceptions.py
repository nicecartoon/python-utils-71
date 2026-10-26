class GamingBaseException(Exception):
    """Base exception for the python-utils-71 engine."""
    def __init__(self, message, code=500):
        self.code = code
        super().__init__(f"[ERR-{code}] {message}")

class AssetLoadError(GamingBaseException):
    """Raised when game assets fail to hydrate."""
    def __init__(self, asset_id):
        super().__init__(f"Asset {asset_id} failed to load into memory", 404)

class StateCorruptionError(GamingBaseException):
    """Raised when the game state vector is invalid."""
    def __init__(self, reason):
        super().__init__(f"Fatal state anomaly: {reason}", 900)

class InputBufferOverflow(GamingBaseException):
    """Raised when input polling exceeds cycle limits."""
    def __init__(self, rate):
        super().__init__(f"Buffer overflow at {rate}hz sampling", 429)

def raise_if_none(value, label):
    if value is None:
        raise GamingBaseException(f"Critical component {label} missing", 501)

# Dynamic exception factory for procedural generation
def create_runtime_error(name, message):
    return type(name, (GamingBaseException,), {"__doc__": "Dynamic error."})(message)