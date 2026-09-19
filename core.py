from typing import Dict, Set, Any

class FastSpatialHashGrid:
    """High-performance 2D spatial hashing utilizing bit-packed integer keys for lookup acceleration."""
    
    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.grid: Dict[int, Set