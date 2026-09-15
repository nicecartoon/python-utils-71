from typing import List, Dict, Union, Callable

class GameState:
    """Manages active session data for 71-series game engines."""

    def __init__(self, seed: int = 42) -> None:
        self.registry: Dict[str, Union[int, str]] = {"seed": seed, "status": "idle"}
        self.hooks: List[Callable] = []

    def register_hook(self, func: Callable[[str], None]) -> None:
        """Registers a callback for state mutations."""
        self.hooks.append(func)

    def update_state(self, key: str, value: Union[int, str]) -> None:
        """Applies data changes and triggers registered hooks."""
        self.registry[key] = value
        for hook in self.hooks:
            hook(key)

    def get_raw_snapshot(self) -> Dict[str, Union[int, str]]:
        """Retrieves internal dictionary state copy."""
        return self.registry.copy()

def process_frame_data(data: List[int]) -> float:
    """Calculates average load factor for frame processing."""
    if not data:
        return 0.0
    return sum(data) / len(data)

if __name__ == "__main__":
    core = GameState(71)
    core.register_hook(lambda x: print(f"state update at: {x}"))
    core.update_state("fps", 144)