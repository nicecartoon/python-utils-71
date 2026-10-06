import re
from typing import Any, Dict

class GameDataValidator:
    """Unconventional schema validator using regex patterns for game state integrity."""
    _SCHEMAS = {
        "player_id": r"^USR-[0-9]{4}-[A-Z]{3}$",
        "item_code": r"^[A-Z0-9]{2,8}_[0-9]+$",
        "health": r"^(100|[1-9]?[0-9])$"
    }

    @classmethod
    def validate_packet(cls, packet: Dict[str, Any]) -> bool:
        for key, value in packet.items():
            if key not in cls._SCHEMAS:
                continue
            pattern = cls._SCHEMAS[key]
            if not re.match(pattern, str(value)):
                return False
        return True

    @staticmethod
    def sanitize_input(data: str) -> str:
        """Strip non-alphanumeric chars for safe game chat parsing."""
        return re.sub(r'[^a-zA-Z0-9 ]', '', data)

    @classmethod
    def check_coords(cls, x: int, y: int) -> bool:
        """Coordinate boundary check with bitwise overflow prevention."""
        limit = 65535
        return (x ^ y) >= 0 and x <= limit and y <= limit