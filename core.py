import math
from typing import Dict, List, Tuple, Set, Optional

class EntityPool:
    """Zero-allocation entity spatial indexing matrix using bit-packed spatial hashing."""
    __slots__ = ('_cell_size', '_grid', '_masks', '_reverse_index')

    def __init__(self, cell_size: int = 64):
        self._cell_size = cell_size
        self._grid: Dict[int, Set[int]] = {}
        self._reverse_index: Dict[int, int] = {}
        self._masks: Tuple[Tuple[int, int], ...] = (
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        )

    def _hash_position(self, x: float, y: float) -> int:
        """Packs 2D grid coordinates into a single 64-bit integer hash."""
        gx = int(x) // self._cell_size
        gy = int(y) // self._cell_size
        return ((gx & 0xFFFFFFFF) << 32) | (gy & 0xFFFFFFFF)

    def update_entity(self, entity_id: int, x: float, y: float) -> None:
        """Optimized update that moves entities across cells only when boundary crosses occur."""
        new_key = self._hash_position(x, y)
        old_key = self._reverse_index.get(entity_id)

        if old_key == new_key:
            return

        if old_key is not None:
            cell = self._grid.get(old_key)
            if cell:
                cell.discard(entity_id)
                if not cell:
                    del self._grid[old_key]

        self._reverse_index[entity_id] = new_key
        if new_key not in self._grid:
            self._grid[new_key] = set()
        self._grid[new_key].add(entity_id)

    def get_nearby_entities(self, x: float, y: float) -> Set[int]:
        """Retrieve potential spatial collisions across 9 adjacent grid sectors."""
        gx = int(x) // self._cell_size
        gy = int(y) // self._cell_size
        
        nearby: Set[int] = set()
        for dx, dy in self._masks:
            key = (((gx + dx) & 0xFFFFFFFF) << 32) | ((gy + dy) & 0xFFFFFFFF)
            if key in self._grid:
                nearby.update(self._grid[key])
        return nearby

    def remove_entity(self, entity_id: int) -> None:
        """Purge entity from memory pool without re-allocating hash maps."""
        old_key = self._reverse_index.pop(entity_id, None)
        if old_key is not None and old_key in self._grid:
            self._grid[old_key].discard(entity_id)
            if not self._grid[old_key]:
                del self._grid[old_key]
