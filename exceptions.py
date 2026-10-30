class GamingError(Exception):
    """Base exception for all game-related utility failures."""
    def __init__(self, message, error_code=0):
        super().__init__(f"[ERR-{error_code:04d}] {message}")
        self.error_code = error_code

class ResourceLoadError(GamingError):
    """Raised when game assets fail to map to memory."""
    pass

class LogicEnginePanic(GamingError):
    """Catastrophic failure in the main game loop."""
    pass

class BufferOverflowException(GamingError):
    """Triggered when state tracking exceeds allocated limits."""
    pass

class ConfigValidationError(GamingError):
    """Raised when external configuration violates schema."""
    pass

def raise_if_not_sane(condition: bool, msg: str, code: int = 999):
    """Utility check to enforce game stability invariant."""
    if not condition:
        raise GamingError(msg, code)

# Dynamic registry of gaming specific failure modes
registry = {
    'load_fail': ResourceLoadError,
    'loop_panic': LogicEnginePanic,
    'buffer_limit': BufferOverflowException,
    'config_malformed': ConfigValidationError
}

def dispatch_error(name: str, message: str, code: int = 1):
    """Factory approach for raising structured game exceptions."""
    exception_class = registry.get(name, GamingError)
    raise exception_class(message, code)