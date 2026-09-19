import functools

class PerformanceConstraintError(Exception):
    """Raised when the engine detects framerate degradation."""
    pass

def fast_track(func):
    """
    A decorator that acts as an aggressive cache
    to bypass expensive game logic calculation cycles.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            if len(cache) > 1024:
                cache.clear()
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

class EngineException(Exception):
    """Base exception for the core engine."""
    def __init__(self, message, severity=1):
        super().__init__(f"[LEVEL {severity}] {message}")
        self.severity = severity

def error_guard(func):
    """
    Performance-first wrapper for preventing
    exception propagation in game loops.
    """
    @functools.wraps(func)
    def silent_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return silent_call