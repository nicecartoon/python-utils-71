import math
from typing import Dict, Any


class GlitchRecoveryManager:
    """Handles edge cases in game physics and stats by auto-correcting corrupted data."""

    def __init__(self, spawn_point: tuple = (0.0, 0.0)):
        self.spawn_point = spawn_point
        self.glitch_log: list[str] = []

    def sanitize_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Process entity state and patch anomalous or corrupted values."""
        try:
            x, y = entity.get("position", self.spawn_point)
            if not (math.isfinite(x) and math.isfinite(y)):
                entity["position"] = self.spawn_point
                self.glitch_log.append(f"Entity '{entity.get('id', 'unknown')}' coordinate reset.")

            hp = entity.get("hp", 100)
            max_hp = max(1, entity.get("max_hp", 100))
            if isinstance(hp, (int, float)):
                if math.isnan(hp) or hp < 0:
                    entity["hp"] = 0
                elif hp > max_hp * 10:
                    entity["hp"] = max_hp
            else:
                entity["hp"] = max_hp

            inventory = entity.get("inventory", {})
            for item, count in list(inventory.items()):
                if not isinstance(count, int) or count <= 0:
                    del inventory[item]
                    self.glitch_log.append(f"Purged ghost item '{item}' from entity.")

        except Exception as err:
            entity.update({"position": self.spawn_point, "hp": 100, "inventory": {}})
            self.glitch_log.append(f"Critical state reset triggered: {err}")

        return entity


def safe_damage_calculator(
    attacker_power: float, defender_armor: float, multiplier: float = 1.0
) -> int:
    """Calculate damage while safely mitigating divide-by-zero, NaN, and float overflow."""
    try:
        if any(not math.isfinite(v) for v in (attacker_power, defender_armor, multiplier)):
            return 0

        armor_effective = max(0.0, defender_armor)
        base_damage = max(0.0, attacker_power - (armor_effective * 0.5))
        final_damage = base_damage * max(0.0, multiplier)

        return min(999999, int(math.floor(final_damage)))
    except (TypeError, ValueError, OverflowError):
        return 0
