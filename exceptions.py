from typing import Optional, Any

class GamingException(Exception):
    """Base exception for the python-utils-71 gaming suite."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class AssetLoadError(GamingException):
    """Raised when a game resource fails to load into memory."""
    def __str__(self) -> str:
        return f"[ASSET_FAIL] {super().__str__()} | Context: {self.context}"

class StateSyncError(GamingException):
    """Raised when game state client and server diverge."""
    def __init__(self, expected: Any, actual: Any) -> None:
        super().__init__(f"State mismatch: expected {expected}, got {actual}")

def raise_if_none(value: Optional[Any], error_cls: type[Exception], msg: str) -> None:
    """Polymorphic guard for null-check state validation."""
    if value is None:
        raise error_cls(msg)

class FrameDropWarning(Warning):
    """Non-fatal notification for frame budget overages."""
    pass