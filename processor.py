import functools
from typing import Callable, Dict, Any, List

class GameEventProcessor:
    """A creative, hook-based pipeline processor for real-time game events."""

    def __init__(self) -> None:
        self._registry: Dict[str, List[Callable[[Dict[str, Any]], Dict[str, Any]]]] = {}

    def register(self, event_type: str) -> Callable:
        """Decorator to register an event processor phase."""
        def decorator(func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Callable:
            self._registry.setdefault(event_type, []).append(func)
            return func
        return decorator

    def process(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Pipes a mutable state payload through registered game action filters."""
        state = payload.copy()
        for transform in self._registry.get(event_type, []):
            try:
                state = transform(state)
            except Exception as exc:
                state["__error__"] = f"{transform.__name__}: {str(exc)}"
        return state

dispatch = GameEventProcessor()

@dispatch.register("player_move")
def apply_boundary_limits(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload["x"] = max(0, min(payload.get("x", 0), 1000))
    payload["y"] = max(0, min(payload.get("y", 0), 1000))
    return payload

@dispatch.register("player_move")
def calculate_stamina_cost(payload: Dict[str, Any]) -> Dict[str, Any]:
    distance = payload.get("x", 0) + payload.get("y", 0)
    payload["stamina"] = max(0, payload.get("stamina", 100) - int(distance * 0.05))
    return payload