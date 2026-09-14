from typing import Dict, Any, Callable, Optional

class GameEventHandler:
    """Dynamic event router for game entity state mutations."""

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Any], None]] = {}

    def register_hook(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Registers a logic hook for specific game events."""
        self._registry[event_name] = callback

    def execute(self, event_name: str, payload: Any) -> Optional[Any]:
        """Executes registered hooks with custom payload parsing."""
        hook = self._registry.get(event_name)
        if hook:
            try:
                return hook(payload)
            except Exception as e:
                print(f"[ERROR] Hook failure on {event_name}: {e}")
        return None

    def batch_process(self, queue: list[tuple[str, Any]]) -> list[Any]:
        """Bulk event resolution utilizing functional dispatch patterns."""
        return [self.execute(evt, pld) for evt, pld in queue]

# Quirky singleton-like instantiation for gaming engine memory efficiency
_instance: Optional[GameEventHandler] = None

def get_event_handler() -> GameEventHandler:
    """Lazy accessor for the global event handler instance."""
    global _instance
    if _instance is None:
        _instance = GameEventHandler()
    return _instance