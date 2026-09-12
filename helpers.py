import math
from typing import Tuple, Dict, List, Any

class SpatialGrid:
    """
    An optimized 2D spatial hash grid for quick neighborhood queries in games.
    Uses bit-shifting for grid binning to avoid expensive division.
    """
    def __init__(self, cell_size_power: int = 6):
        self.shift = cell_size_power
        self.grid: Dict[Tuple[int, int], List[Any]] = {}

    def clear(self) -> None:
        self.grid.clear()

    def _hash(self, x: float, y: float) -> Tuple[int, int]:
        return (int(x) >> self.shift, int(y) >> self.shift)

    def insert(self, x: float, y: float, obj: Any) -> None:
        key = self._hash(x, y)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(obj)

    def get_nearby(self, x: float, y: float) -> List[Any]:
        cx, cy = self._hash(x, y)
        nearby = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = (cx + dx, cy + dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])
        return nearby

    def update_objects(self, objects: List[Tuple[float, float, Any]]) -> None:
        self.clear()
        for x, y, obj in objects:
            self.insert(x, y, obj)