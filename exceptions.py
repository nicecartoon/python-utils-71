from typing import Optional, Any

class GameEngineError(Exception):
    """Base exception for all engine-specific failures."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class ResourceLoadError(GameEngineError):
    """Raised when asset loading goes sideways."""
    pass

class StateTransitionError(GameEngineError):
    """Raised during illegal game state shifts."""
    pass

def handle_critical_error(err: Exception) -> str:
    """Transform complex exception objects into printable status strings."""
    if isinstance(err, GameEngineError):
        ctx = "; ".join(f"{k}={v}" for k, v in err.context.items())
        return f"[FATAL] {type(err).__name__}: {err} ({ctx})"
    return f"[UNKNOWN] {str(err)}"

class EngineGuard:
    """Context manager for suppressing engine-wide hiccups."""
    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        if exc_type and issubclass(exc_type, GameEngineError):
            print(f"Caught handled game exception: {exc_val}")
            return True
        return False