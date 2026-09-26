import array
from typing import List, Tuple

class BitwiseSpatialGrid:
    """High-performance 2D spatial partitioning grid using bit-packed coordinates."""
    
    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self._shift = cell_size.bit_length() - 1
        self._buckets = {}
        self._dirty_cells = set()

    def _pack_coords(self, x: float, y: float) -> int:
        cx = int(x) >> self._shift
        cy = int(y) >> self._shift
        return (cx << 16) | (cy & 0xFFFF)

    def insert(self, entity_id: int, x: float, y: float) -> int:
        cell_key = self._pack_coords(x, y)
        bucket = self._buckets.setdefault(cell_key, array.array('i'))
        bucket.append(entity_id)
        self._dirty_cells.add(cell_key)
        return cell_key

    def bulk_insert(self, entities: List[Tuple[int, float, float]]) -> None:
        for eid, x, y in entities:
            ck = self._pack_coords(x, y)
            bucket = self._buckets.setdefault(ck, array.array('i'))
            bucket.append(eid)

    def query_radius(self, x: float, y: float, radius: float) -> List[int]:
        min_x, max_x = int(x - radius) >> self._shift, int(x + radius) >> self._shift
        min_y, max_y = int(y - radius) >> self._shift, int(y + radius) >> self._shift
        
        results = array.array('i')
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                key = (cx << 16) | (cy & 0xFFFF)
                bucket = self._buckets.get(key)
                if bucket:
                    results.extend(bucket)
        return list(results)

    def clear(self) -> None:
        self._buckets.clear()
        self._dirty_cells.clear()