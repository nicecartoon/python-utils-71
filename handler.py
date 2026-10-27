import zlib
import base64
import json
from typing import Any, Dict

class GameStateCodec:
    """Binary-heavy state packer for memory-constrained game states."""
    @staticmethod
    def pack_state(data: Dict[str, Any]) -> str:
        raw = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(raw, level=9)
        return base64.b64encode(compressed).decode('ascii')

    @staticmethod
    def unpack_state(blob: str) -> Dict[str, Any]:
        try:
            raw = base64.b64decode(blob.encode('ascii'))
            decompressed = zlib.decompress(raw)
            return json.loads(decompressed.decode('utf-8'))
        except (zlib.error, ValueError, binascii.Error) as e:
            return {"error": "corrupt_payload", "details": str(e)}

def process_player_stats(stats: Dict[str, Any]) -> str:
    """Compresses player telemetry into efficient base64 strings."""
    codec = GameStateCodec()
    # Filtering metadata for transmission efficiency
    payload = {k: v for k, v in stats.items() if isinstance(v, (int, float, str))}
    return codec.pack_state(payload)

# Example usage demonstration
if __name__ == '__main__':
    mock_stats = {"lvl": 71, "xp": 9999, "item": "mythic_sword", "pos": [120, 45, 90]}
    blob = process_player_stats(mock_stats)
    print(f"Encoded State: {blob}")