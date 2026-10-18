import math
from typing import Dict, Any, List, Tuple


class BitPackedGameData:
    """Encodes and decodes multi-stat game entity states into tightly packed byte streams."""

    DEFAULT_SCHEMA: List[Tuple[str, int]] = [
        ("health", 8),       # 0-255
        ("mana", 8),         # 0-255
        ("level", 7),        # 0-127
        ("is_poisoned", 1),  # 0-1
        ("is_buffed", 1),    # 0-1
        ("element_type", 3), # 0-7
        ("facing_deg", 9),   # 0-511
        ("kill_count", 11)   # 0-2047
    ]

    def __init__(self, schema: List[Tuple[str, int]] = None):
        self.schema = schema or self.DEFAULT_SCHEMA
        self.total_bits = sum(bits for _, bits in self.schema)
        self.byte_count = (self.total_bits + 7) // 8

    def pack(self, stats: Dict[str, int]) -> bytes:
        """Packs gaming stats dict into compact binary stream using bitwise composition."""
        bit_accumulator = 0
        current_shift = 0

        for name, bits in self.schema:
            max_val = (1 << bits) - 1
            val = min(max(0, stats.get(name, 0)), max_val)
            bit_accumulator |= (val << current_shift)
            current_shift += bits

        return bit_accumulator.to_bytes(self.byte_count, byteorder="big")

    def unpack(self, raw_bytes: bytes) -> Dict[str, int]:
        """Unpacks binary stream back into game stats dictionary."""
        bit_accumulator = int.from_bytes(raw_bytes, byteorder="big")
        stats = {}
        current_shift = 0

        for name, bits in self.schema:
            mask = (1 << bits) - 1
            stats[name] = (bit_accumulator >> current_shift) & mask
            current_shift += bits

        return stats


def compressed_spatial_hash(x: float, y: float, cell_size: float = 16.0) -> int:
    """Creative spatial hashing for 2D gaming grid alignment using Cantor pairing variant."""
    gx, gy = int(x // cell_size), int(y // cell_size)
    u = gx * 2 if gx >= 0 else -gx * 2 - 1
    v = gy * 2 if gy >= 0 else -gy * 2 - 1
    return ((u + v) * (u + v + 1)) // 2 + v
