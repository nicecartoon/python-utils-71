from typing import Dict, List, Any, Union, Callable

class GameActionHandler:
    def __init__(self, registry: Dict[str, Callable[[Any], None]]) -> None:
        """Initialize handler with a registry of game-state mutation functions."""
        self._registry: Dict[str, Callable[[Any], None]] = registry

    def execute(self, action_name: str, payload: Union[int, str, dict]) -> None:
        """Dispatch game events to their registered logic components."""
        action = self._registry.get(action_name)
        if action:
            try:
                action(payload)
            except Exception as e:
                self._log_error(action_name, e)

    def _log_error(self, name: str, err: Exception) -> None:
        """Internal diagnostic logging for failed state mutations."""
        print(f"[ERROR] action '{name}' failed with exception: {err}")

def create_handler(commands: List[str]) -> GameActionHandler:
    """Factory function returning a configured handler instance."""
    mapping: Dict[str, Callable[[Any], None]] = {
        cmd: (lambda x: print(f"Processing {cmd}: {x}")) for cmd in commands
    }
    return GameActionHandler(mapping)

if __name__ == "__main__":
    handler = create_handler(['spawn', 'despawn', 'level_up'])
    handler.execute('spawn', {'id': 101, 'type': 'dragon'})