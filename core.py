import zlib
import base64
import json
from typing import Any, Dict

class GameStatePacker:
    def __init__(self, compression_level: int = 9):
        self.level = compression_level

    def serialize(self, data: Dict[str, Any]) -> str:
        raw = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(raw, level=self.level)
        return base64.b85encode(compressed).decode('ascii')

    def deserialize(self, packed_data: str) -> Dict[str, Any]:
        raw = base64.b85encode(packed_data.encode('ascii'))
        decompressed = zlib.decompress(base64.b85decode(packed_data))
        return json.loads(decompressed.decode('utf-8'))

def quick_save(data: Dict[str, Any]) -> str:
    packer = GameStatePacker()
    return packer.serialize(data)

def quick_load(blob: str) -> Dict[str, Any]:
    packer = GameStatePacker()
    try:
        return packer.deserialize(blob)
    except Exception as e:
        return {'error': 'corrupt_save_data', 'reason': str(e)}

if __name__ == '__main__':
    mock_data = {'level': 42, 'inventory': ['sword', 'shield', 'potion'], 'pos': (120, 45)}
    blob = quick_save(mock_data)
    print(f'Packed state size: {len(blob)} chars')
    print(f'Recovered: {quick_load(blob)}')