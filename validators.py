import re
from typing import Any, Callable, Dict, Optional

class InputGuard:
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            'player_id': lambda x: isinstance(x, int) and 0 < x < 99999,
            'command': lambda x: isinstance(x, str) and bool(re.match(r'^[a-z_]{3,15}$', x)),
            'latency': lambda x: isinstance(x, (int, float)) and 0 <= x < 500
        }

    def validate(self, schema: Dict[str, Any]) -> bool:
        try:
            return all(self._rules[key](value) for key, value in schema.items())
        except KeyError:
            return False

    @staticmethod
    def sanitize_input(data: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '', data)[:20]

def process_packet(raw_data: dict, validator: InputGuard) -> Optional[dict]:
    if not validator.validate(raw_data):
        return None
    return {k: v for k, v in raw_data.items()}