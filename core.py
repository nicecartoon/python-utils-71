class SpatialGridOptimizer:
    __slots__ = ('cell_size', 'shift', 'grid')

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.shift = cell_size.bit_length() - 1
        if (1 << self.shift) != cell_size:
            raise ValueError('Cell size must be a power of 2 for shift optimization')
        self.grid = {}

    def clear(self) -> None:
        self.grid.clear()

    def update_entities(self, entities: list) -> None:
        grid = self.grid
        shift = self.shift
        grid.clear()

        for entity in entities:
            cx = int(entity.x) >> shift
            cy = int(entity.y) >> shift
            key = (cx << 16) | (cy & 0xFFFF)

            if key not in grid:
                grid[key] = []
            grid[key].append(entity)

    def query_range(self, x: float, y: float, radius: float) -> list:
        shift = self.shift
        grid = self.grid
        results = []
        results_extend = results.extend

        min_cx = int(x - radius) >> shift
        max_cx = int(x + radius) >> shift
        min_cy = int(y - radius) >> shift
        max_cy = int(y + radius) >> shift

        for cx in range(min_cx, max_cx + 1):
            packed_cx = cx << 16
            for cy in range(min_cy, max_cy + 1):
                key = packed_cx | (cy & 0xFFFF)
                cell = grid.get(key)
                if cell:
                    results_extend(cell)
        return results