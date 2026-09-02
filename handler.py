from typing import Dict, List, Callable, Tuple
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class Player:
    """Player entity with stats for the game."""
    name: str
    health: int
    score: int

class Action(Enum):
    """Enumeration of possible game actions."""
    ATTACK = auto()
    DEFEND = auto()
    HEAL = auto()

def attack_handler(player: Player, enemy_strength: int) -> Tuple[Player, str]:
    """Process attack action.

    Reduces health based on enemy strength and adds to score if survived.
    """
    damage: int = enemy_strength
    player.health -= damage
    msg: str = f"Attacked enemy, received {damage} damage."
    if player.health > 0:
        player.score += 5
    return player, msg

def defend_handler(player: Player, _: int) -> Tuple[Player, str]:
    """Process defend action.

    Increases health slightly.
    """
    player.health += 3
    return player, "Defended successfully, health increased."

def heal_handler(player: Player, _: int) -> Tuple[Player, str]:
    """Process heal action.

    Restores a fixed amount of health.
    """
    player.health += 10
    return player, "Healed for 10 health points."

ACTION_HANDLERS: Dict[Action, Callable[[Player, int], Tuple[Player, str]]] = {
    Action.ATTACK: attack_handler,
    Action.DEFEND: defend_handler,
    Action.HEAL: heal_handler,
}

def handle_action(player: Player, action: Action, enemy_strength: int = 10) -> Tuple[Player, str]:
    """Handle a single game action using registered handler.

    Uses a mapping for extensibility, unusual for simple cases but flexible.
    """
    if action not in ACTION_HANDLERS:
        return player, "Invalid action."
    handler: Callable[[Player, int], Tuple[Player, str]] = ACTION_HANDLERS[action]
    return handler(player, enemy_strength)

def process_game_sequence(player: Player, actions: List[Action]) -> List[str]:
    """Process a sequence of actions for the player.

    Returns list of result messages. Modifies player in place.
    """
    results: List[str] = []
    for action in actions:
        player, message = handle_action(player, action)
        results.append(message)
    return results

if __name__ == "__main__":
    hero: Player = Player("Knight", 80, 0)
    sequence: List[Action] = [Action.ATTACK, Action.HEAL, Action.DEFEND, Action.ATTACK]
    messages: List[str] = process_game_sequence(hero, sequence)
    print("Game results:", messages)
    print(f"Final stats - Health: {hero.health}, Score: {hero.score}")