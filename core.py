import math
from typing import Dict, List, Set, Tuple


class SpatialEntityGrid:
    """Fast spatial hash grid utilizing bitwise coordinate packing for gaming entities."""

    __slots__ = ("_cell_size", "_bit_shift", "_grid")

    def __init__(self, cell_size: int = 32):
        self._cell_size = cell_size
        self._bit_shift = 16  # Supports coord ranges -32768 to 32767
        self._grid: Dict[int, Set[int]] = {}

    def _hash_coords(self, x: float, y: float) -> int:
        cx = (int(x) // self._cell_size) + 32768
        cy = (int(y) // self._cell_size) + 32768
        return (cx << self._bit_shift) | cy

    def update_entity(
        self, entity_id: int, old_pos: Tuple[float, float], new_pos: Tuple[float, float]
    ) -> None:
        old_hash = self._hash_coords(*old_pos)
        new_hash = self._hash_coords(*new_pos)

        if old_hash != new_hash:
            if old_hash in self._grid:
                self._grid[old_hash].discard(entity_id)
                if not self._grid[old_hash]:
                    del self._grid[old_hash]

            if new_hash not in self._grid:
                self._grid[new_hash] = set()
            self._grid[new_hash].add(entity_id)

    def query_radius(self, x: float, y: float, radius: float) -> List[int]:
        min_x = int(x - radius) // self._cell_size + 32768
        max_x = int(x + radius) // self._cell_size + 32768
        min_y = int(y - radius) // self._cell_size + 32768
        max_y = int(y + radius) // self._cell_size + 32768

        nearby_entities: List[int] = []

        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                key = (cx << self._bit_shift) | cy
                if key in self._grid:
                    nearby_entities.extend(self._grid[key])

        return nearby_entities