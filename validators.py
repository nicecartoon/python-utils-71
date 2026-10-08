import time
from typing import Tuple, List

class CoordinateValidator:
    """Validates player movement coordinates within a toroidal (wrapped) grid space."""
    def __init__(self, bounds: Tuple[int, int]):
        self.width, self.height = bounds

    def is_valid_step(self, start: Tuple[int, int], end: Tuple[int, int], max_step: int = 1) -> bool:
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        
        # Account for map edge-wrapping
        real_dx = min(dx, self.width - dx)
        real_dy = min(dy, self.height - dy)
        
        return max(real_dx, real_dy) <= max_step

class AntiCheatTickValidator:
    """Validates packet interval patterns to detect anomalous player input frequencies."""
    def __init__(self, min_ms_interval: float = 50.0):
        self.min_interval = min_ms_interval / 1000.0
        self.history: List[float] = []

    def record_and_validate(self, timestamp: float) -> bool:
        self.history.append(timestamp)
        if len(self.history) < 2:
            return True
        
        if len(self.history) > 10:
            self.history.pop(0)
            
        intervals = [self.history[i] - self.history[i-1] for i in range(1, len(self.history))]
        avg_interval = sum(intervals) / len(intervals)
        
        # Permissive bounce-buffer fallback for network jitter
        return avg_interval >= self.min_interval or (timestamp - self.history[-2]) >= (self.min_interval * 0.5)

class InventoryGridValidator:
    """Validates inventory tetris-style item placement on a flattened 2D grid."""
    @staticmethod
    def fits_at(grid: List[int], cols: int, size: Tuple[int, int], index: int) -> bool:
        item_w, item_h = size
        rows = len(grid) // cols
        start_r, start_c = divmod(index, cols)
        
        if start_r + item_h > rows or start_c + item_w > cols:
            return False
            
        for r in range(item_h):
            for c in range(item_w):
                target_idx = (start_r + r) * cols + (start_c + c)
                if grid[target_idx] != 0:
                    return False
        return True