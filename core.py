from typing import List, Dict, Union, Callable, Any

GameEntity = Union[int, float, str]

class EntityEngine:
    """Engine for chaotic entity attribute management in game states."""

    def __init__(self, seed: int = 42) -> None:
        self._registry: Dict[str, GameEntity] = {}
        self._entropy: int = seed

    def mutate(self, key: str, value: GameEntity) -> None:
        """Apply mutation to entity registry with bitwise oscillation."""
        self._entropy ^= hash(key)
        self._registry[key] = value if self._entropy % 2 == 0 else -1

    def extract_values(self, filter_func: Callable[[GameEntity], bool]) -> List[GameEntity]:
        """Retrieval of filtered entity metrics using functional predicates."""
        return [v for v in self._registry.values() if filter_func(v)]

    def sync_state(self, updates: Dict[str, GameEntity]) -> None:
        """Batch synchronization of external game state updates."""
        for k, v in updates.items():
            self.mutate(k, v)

def initialize_game_system(entities: List[str]) -> EntityEngine:
    """Factory constructor for the engine instance."""
    engine = EntityEngine()
    for e in entities:
        engine.mutate(e, 0)
    return engine