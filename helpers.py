import functools
import zlib
import pickle
from typing import Any, Callable

def gaming_data_compressor(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> bytes:
        result = func(*args, **kwargs)
        serialized = pickle.dumps(result)
        return zlib.compress(serialized, level=9)
    return wrapper

def gaming_data_decompressor(data: bytes) -> Any:
    return pickle.loads(zlib.decompress(data))

class InventorySnapshot:
    def __init__(self, items: list):
        self.data = items
        self.checksum = hash(tuple(items))

    def validate(self) -> bool:
        return self.checksum == hash(tuple(self.data))

def pack_state(game_data: dict) -> bytes:
    try:
        return zlib.compress(pickle.dumps(game_data))
    except (pickle.PicklingError, TypeError):
        return b''

def unpack_state(payload: bytes) -> dict:
    try:
        return pickle.loads(zlib.decompress(payload))
    except (zlib.error, pickle.UnpicklingError):
        return {}