from typing import Dict, List, Union, Callable

class GameStateProcessor:
    """Handles transformation of raw game data into usable entities."""

    def __init__(self, multipliers: Dict[str, float]) -> None:
        self._multipliers = multipliers

    def apply_buffs(self, stats: Dict[str, Union[int, float]], tag: str) -> Dict[str, float]:
        """Applies tag-specific multipliers to existing numerical stats."""
        factor: float = self._multipliers.get(tag, 1.0)
        return {k: float(v) * factor for k, v in stats.items()}

    def batch_process(self, data: List[Dict[str, int]], func: Callable[[Dict[str, int]], float]) -> List[float]:
        """Functional processing of game entity lists using a provided strategy."""
        return [func(item) for item in data]

    @staticmethod
    def normalize_score(score: int, cap: int = 1000) -> float:
        """Compresses high scores into a floating point scale for UI display."""
        return min(float(score) / cap, 1.0)

    def __repr__(self) -> str:
        return f"GameStateProcessor(multipliers={list(self._multipliers.keys())})"