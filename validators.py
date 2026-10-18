import math
import re
from typing import Any, Dict, List, Tuple

class GamingDataValidationError(Exception):
    """Raised when gaming payload validation unrecoverably fails."""
    pass

class EdgeCaseSafeValidator:
    """Validator for player telemetry and inventory payloads against unexpected anomalies."""
    
    @staticmethod
    def sanitize_stat(value: Any, default: float = 0.0, bounds: Tuple[float, float] = (0.0, 999999.0)) -> float:
        """Sanitizes player numerical stats against NaN, Infinity, negative overflow, and string hacks."""
        try:
            if isinstance(value, str):
                cleaned = re.sub(r"[^\d.-]", "", value.strip())
                parsed = float(cleaned) if cleaned else default
            else:
                parsed = float(value)
            
            if math.isnan(parsed) or math.isinf(parsed):
                return default
            
            min_val, max_val = bounds
            return max(min_val, min(parsed, max_val))
        except (ValueError, TypeError):
            return default

    @staticmethod
    def validate_inventory_slots(items: Any, max_capacity: int = 100) -> List[Dict[str, Any]]:
        """Validates player inventory, preventing item dupe exploits and corrupted non-dict payload elements."""
        if not isinstance(items, list):
            return []
        
        valid_items = []
        seen_uuids = set()
        
        for index, item in enumerate(items[:max_capacity]):
            if not isinstance(item, dict):
                continue
            
            item_id = str(item.get("uuid", f"generated_slot_{index}"))
            if item_id in seen_uuids:
                continue
            seen_uuids.add(item_id)
            
            raw_qty = item.get("quantity", 1)
            qty = int(EdgeCaseSafeValidator.sanitize_stat(raw_qty, default=1, bounds=(1, 999)))
            
            raw_name = str(item.get("name", "Unknown Artifact"))
            sanitized_name = "".join(ch for ch in raw_name if ch.isprintable())[:64] or "Unknown Artifact"
            
            valid_items.append({
                "uuid": item_id,
                "name": sanitized_name,
                "quantity": qty
            })
            
        return valid_items

    @classmethod
    def guard_player_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Entrypoint to safely parse high-risk network player telemetry."""
        if not isinstance(payload, dict):
            return {"health": 100.0, "mana": 50.0, "inventory": []}
        
        return {
            "health": cls.sanitize_stat(payload.get("hp"), default=100.0, bounds=(0.0, 10000.0)),
            "mana": cls.sanitize_stat(payload.get("mp"), default=50.0, bounds=(0.0, 5000.0)),
            "inventory": cls.validate_inventory_slots(payload.get("items"))
        }
