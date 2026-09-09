import math
from typing import Tuple

class Vector2D:
    """Creative 2D vector representation using complex numbers under the hood."""
    def __init__(self, x: float, y: float):
        self._val = complex(x, y)

    @property
    def x(self) -> float:
        return self._val.real

    @property
    def y(self) -> float:
        return self._val.imag

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        res = self._val + other._val
        return Vector2D(res.real, res.imag)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        res = self._val - other._val
        return Vector2D(res.real, res.imag)

    def scale(self, factor: float) -> 'Vector2D':
        res = self._val * factor
        return Vector2D(res.real, res.imag)

    def magnitude(self) -> float:
        return abs(self._val)

    def rotate(self, degrees: float) -> 'Vector2D':
        radians = math.radians(degrees)
        rotator = complex(math.cos(radians), math.sin(radians))
        res = self._val * rotator
        return Vector2D(res.real, res.imag)

    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y

    def as_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"