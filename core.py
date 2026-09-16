from typing import Dict, Set, List

class Entity:
    __slots__ = ('id', 'position', 'radius')
    def __init__(self, entity_id: int, x: float, y: float, radius: float = 1.0):
        self.id = entity_id
        self.position = complex(x, y)
        self.radius = radius

class SpatialHashGrid:
    __slots__ = ('cell_size', 'grid')

    def __init__(self, cell_size: int = 50):
        self.cell_size = cell_size
        self.grid: Dict[complex, Set[Entity]] = {}

    def _to_cell(self, pos: complex) -> complex:
        return complex(pos.real // self.cell_size, pos.imag // self.cell_size)

    def insert(self, entity: Entity) -> None:
        cell = self._to_cell(entity.position)
        self.grid.setdefault(cell, set()).add(entity)

    def update(self, entity: Entity, old_pos: complex) -> None:
        old_cell = self._to_cell(old_pos)
        new_cell = self._to_cell(entity.position)
        if old_cell != new_cell:
            if old_cell in self.grid:
                self.grid[old_cell].discard(entity)
                if not self.grid[old_cell]:
                    del self.grid[old_cell]
            self.insert(entity)

    def get_nearby_collisions(self, entity: Entity) -> List[Entity]:
        center_cell = self._to_cell(entity.position)
        nearby = []
        offsets = (complex(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        for offset in offsets:
            cell = center_cell + offset
            if cell in self.grid:
                nearby.extend([
                    other for other in self.grid[cell]
                    if other.id != entity.id and abs(other.position - entity.position) <= (entity.radius + other.radius)
                ])
        return nearby