import math
import time
from functools import reduce
from typing import Tuple


class DeltaSmoother:
    """Frame delta time smoother using rolling exponential decay."""

    def __init__(self, alpha: float = 0.15):
        self.alpha = alpha
        self._last_time = time.perf_counter()
        self._smoothed_dt = 1.0 / 60.0

    def tick(self) -> float:
        now = time.perf_counter()
        raw_dt = now - self._last_time
        self._last_time = now
        self._smoothed_dt = (self.alpha * raw_dt) + ((1.0 - self.alpha) * self._smoothed_dt)
        return self._smoothed_dt


def coord_to_chunk_key(x: float, y: float, chunk_size: int = 16) -> int:
    """Packs 2D spatial coordinates into a single 64-bit integer chunk key."""
    cx = math.floor(x) // chunk_size
    cy = math.floor(y) // chunk_size
    return ((cx & 0xFFFFFFFF) << 32) | (cy & 0xFFFFFFFF)


def chunk_key_to_coord(key: int, chunk_size: int = 16) -> Tuple[int, int]:
    """Unpacks 64-bit integer key back to world chunk grid coordinates."""
    cx = (key >> 32) & 0xFFFFFFFF
    if cx & 0x80000000:
        cx -= 0x100000000
    cy = key & 0xFFFFFFFF
    if cy & 0x80000000:
        cy -= 0x100000000
    return cx * chunk_size, cy * chunk_size


def status_bitmask(*effect_indices: int) -> int:
    """Flattens variadic status effect indices into a bitwise flag mask."""
    return reduce(lambda mask, idx: mask | (1 << idx), effect_indices, 0)


def exp_damp(current: float, target: float, smoothing: float, dt: float) -> float:
    """Frame-rate independent exponential lerp decay for smooth camera tracking."""
    return target + (current - target) * math.exp(-smoothing * dt)
