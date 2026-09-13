from typing import Generator, Dict, Set
from math import floor

class SpatialGrid:
    """A spatial hash grid using complex numbers for 2D entity tracking."""
    def __init__(self, cell_size: float = 32.0):
        self.cell_size = float(cell_size)
        self._grid: Dict[complex, Set[object]] = {}

    def _to_cell(self, pos: complex) -> complex:
        return complex(floor(pos.real / self.cell_size), floor(pos.imag / self.cell_size))

    def insert(self, entity: object, pos: complex) -> None:
        cell = self._to_cell(pos)
        self._grid.setdefault(cell, set()).add(entity)

    def move(self, entity: object, old_pos: complex, new_pos: complex) -> None:
        old_cell, new_cell = self._to_cell(old_pos), self._to_cell(new_pos)
        if old_cell != new_cell:
            if old_cell in self._grid:
                self._grid[old_cell].discard(entity)
                if not self._grid[old_cell]:
                    del self._grid[old_cell]
            self.insert(entity, new_pos)

    def query_radius(self, pos: complex, radius: float) -> Generator[object, None, None]:
        min_cell = self._to_cell(pos - complex(radius, radius))
        max_cell = self._to_cell(pos + complex(radius, radius))
        seen = set()
        for x in range(int(min_cell.real), int(max_cell.real) + 1):
            for y in range(int(min_cell.imag), int(max_cell.imag) + 1):
                cell = complex(x, y)
                for entity in self._grid.get(cell, ()):
                    if entity not in seen:
                        seen.add(entity)
                        yield entity
