import logging
from dataclasses import dataclass
from typing import Any, Dict, Tuple

@dataclass
class PlayerState:
    health: int = 100
    position: Tuple[int, int] = (0, 0)
    inventory: list = None

    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []

class GameProcessor:
    def __init__(self, map_bounds: Tuple[int, int] = (100, 100)):
        self.states: Dict[str, PlayerState] = {}
        self.map_bounds = map_bounds
        self.logger = logging.getLogger("game.processor")

    def _get_or_create_state(self, player_id: str) -> PlayerState:
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player identifier")
        if player_id not in self.states:
            self.states[player_id] = PlayerState()
        return self.states[player_id]

    def process_position_update(self, player_id: str, pos: Any) -> Dict[str, Any]:
        try:
            state = self._get_or_create_state(player_id)
            if not isinstance(pos, (list, tuple)) or len(pos) != 2:
                raise TypeError("Position requires exactly two coordinates")
            try:
                x = int(pos[0])
                y = int(pos[1])
            except (ValueError, TypeError):
                raise ValueError("Coordinates must be convertible to integers")
            if x < 0 or y < 0 or x >= self.map_bounds[0] or y >= self.map_bounds[1]:
                raise IndexError("Position exceeds game map boundaries")
            state.position = (x, y)
            if state.health < 20:
                self.logger.warning(f"Player {player_id} moving with critical health")
            return {"success": True, "new_position": state.position}
        except (ValueError, TypeError, IndexError) as err:
            self.logger.error(f"Position update failed for {player_id}: {err}")
            return {"success": False, "error": str(err), "type": type(err).__name__}
        except Exception as err:
            self.logger.critical(f"Unexpected failure: {err}")
            return {"success": False, "error": "system error"}

    def apply_item_effect(self, player_id: str, item: Dict[str, Any]) -> Dict[str, Any]:
        try:
            state = self._get_or_create_state(player_id)
            if not isinstance(item, dict):
                raise TypeError("Item must be a dictionary")
            effect = item.get("effect")
            value = item.get("value", 0)
            if effect == "heal":
                if not isinstance(value, (int, float)) or value <= 0:
                    raise ValueError("Heal value must be positive number")
                state.health = min(100, state.health + int(value))
            elif effect == "damage":
                if not isinstance(value, (int, float)) or value < 0:
                    raise ValueError("Damage value must be non-negative")
                state.health = max(0, state.health - int(value))
                if state.health == 0:
                    state.inventory.clear()
            else:
                raise KeyError("Unsupported item effect")
            return {"success": True, "health": state.health}
        except (ValueError, TypeError, KeyError) as err:
            return {"success": False, "error": str(err)}
        except Exception:
            return {"success": False, "error": "effect application error"}

if __name__ == "__main__":
    processor = GameProcessor()
    print(processor.process_position_update("hero1", [45, 67]))
    print(processor.apply_item_effect("hero1", {"effect": "heal", "value": 30}))
    print(processor.process_position_update("hero1", [-1, 50]))
    print(processor.apply_item_effect("hero1", {"effect": "damage", "value": 200}))
    print(processor.apply_item_effect("hero1", "invalid"))