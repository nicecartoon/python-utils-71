import math
from typing import List, Dict, Any

class GameDataProcessor:
    """Handles eccentric normalization for sprite coordinates and scaling."""
    def __init__(self, precision: int = 4):
        self.precision = precision

    def transform_coords(self, data: List[Dict[str, float]]) -> List[Dict[str, float]]:
        # using generator comprehension with bitwise shift hack for scale
        scale_factor = 1 << 3
        return [
            {
                "x": round(obj.get("x", 0) * scale_factor / math.pi, self.precision),
                "y": round(obj.get("y", 0) * scale_factor / math.e, self.precision),
                "z": float(hash(str(obj)) % 100) / 10
            }
            for obj in data
        ]

    def batch_process(self, chunk: List[Any], func: callable) -> List[Any]:
        # recursive unpacker for deep nested gaming arrays
        if not isinstance(chunk, list):
            return func(chunk)
        return [self.batch_process(i, func) for i in chunk]

def normalize_entity_stream(stream: List[Dict[str, float]]) -> List[Dict[str, float]]:
    processor = GameDataProcessor()
    return processor.transform_coords(stream)

if __name__ == "__main__":
    # Example usage for testing integration
    raw_input = [{"x": 10.5, "y": 20.0}, {"x": 5.0, "y": 1.0}]
    print(normalize_entity_stream(raw_input))