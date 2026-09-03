class GamingBaseException(Exception):
    """Root exception for python-utils-71."""
    pass

class ResourceLoadingError(GamingBaseException):
    """Raised when game assets fail to load."""
    def __init__(self, resource_path, reason):
        self.msg = f"Failed to load asset at {resource_path}: {reason}"
        super().__init__(self.msg)

class StateTransitionError(GamingBaseException):
    """Invalid state switch for game entities."""
    def __init__(self, current, target):
        super().__init__(f"Illegal transition from {current} to {target}")

class LogicConsistencyError(GamingBaseException):
    """Unexpected game engine state anomaly."""
    def __init__(self, context):
        self.context = context
        super().__init__(f"Engine inconsistency detected: {context}")

def raise_if_none(value, message):
    if value is None:
        raise GamingBaseException(message)

class ExceptionFactory:
    _registry = {
        'load': ResourceLoadingError,
        'state': StateTransitionError,
        'logic': LogicConsistencyError
    }

    @classmethod
    def trigger(cls, kind, *args):
        exc_class = cls._registry.get(kind, GamingBaseException)
        raise exc_class(*args)