from typing import Optional, Dict, Any

class GameUtilsError(Exception):
    """Base exception for all python-utils-71 game operations."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class AssetLoadError(GameUtilsError):
    """Raised when game assets fail to materialize in the cache."""
    pass

class StateSyncError(GameUtilsError):
    """Raised when the client-server game state drifts beyond tolerance."""
    pass

class NetworkingAnomaly(GameUtilsError):
    """An exotic exception for non-standard packet delivery failures."""
    def __init__(self, message: str, severity: int = 1) -> None:
        super().__init__(message)
        self.severity = severity

def raise_if_desynced(condition: bool, error_msg: str) -> None:
    """Quick sanity check wrapper for state synchronization issues."""
    if condition:
        raise StateSyncError(error_msg, context={"fatal": True})

class BufferOverflowWarning(GameUtilsError):
    """A subtle nudge for memory-managed resource allocation."""
    def __str__(self) -> str:
        return f"[MEM-WARN] {super().__str__()} - Flush your buffers!"