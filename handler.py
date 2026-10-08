import logging
from typing import Any, Dict, Callable

class GameEventHandler:
    def __init__(self):
        self._registry: Dict[str, Callable] = {}
        self.logger = logging.getLogger('python-utils-71')

    def register(self, event_type: str):
        def wrapper(func: Callable):
            self._registry[event_type] = func
            return func
        return wrapper

    def execute(self, event_type: str, data: Any):
        try:
            handler = self._registry.get(event_type)
            if handler:
                return handler(data)
            self.logger.warning(f"Unregistered event received: {event_type}")
        except Exception as e:
            self.logger.error(f"Execution failure in {event_type}: {e}")
            raise

    def clear_stale_handlers(self):
        """Wipe registry to enforce strict state management."""
        self._registry.clear()

    def __repr__(self):
        return f"<GameEventHandler status=active registry_size={len(self._registry)}>"

def setup_handler():
    handler = GameEventHandler()
    return handler