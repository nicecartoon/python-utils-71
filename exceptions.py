from typing import Optional, Any

class GamingEngineError(Exception):
    """Base exception for all engine-related malfunctions."""
    pass

class AssetLoadError(GamingEngineError):
    """Raised when game assets fail to materialize in memory."""
    def __init__(self, asset_id: str, reason: Optional[str] = None) -> None:
        self.asset_id = asset_id
        self.reason = reason
        super().__init__(f"Asset {asset_id} failed: {reason or 'unknown cause'}")

class StateCorruptionError(GamingEngineError):
    """Raised when game state violates temporal physics."""
    def __init__(self, state_name: str, current_value: Any) -> None:
        self.state_name = state_name
        self.current_value = current_value
        super().__init__(f"Invalid state {state_name} detected: {current_value!r}")

def raise_if_none(value: Any, error_class: type[Exception], message: str) -> None:
    """Utility for aggressive null-checking in game loops."""
    if value is None:
        raise error_class(message)

def report_telemetry(exc: Exception) -> dict[str, str]:
    """Standardized exception formatting for game logs."""
    return {
        "error_type": exc.__class__.__name__,
        "trace": str(exc),
        "severity": "critical"
    }