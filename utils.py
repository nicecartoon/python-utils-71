import random
from typing import List, Dict, Union, Optional

GameStats = Dict[str, Union[int, float]]

def calculate_loot_drop(rarity_weights: Dict[str, float], luck_modifier: float = 1.0) -> str:
    """Determines item rarity based on weight and player luck factor."""
    adjusted_weights = {k: v * luck_modifier for k, v in rarity_weights.items()}
    total = sum(adjusted_weights.values())
    pick = random.uniform(0, total)
    current = 0.0
    for rarity, weight in adjusted_weights.items():
        current += weight
        if pick <= current:
            return rarity
    return "common"

def normalize_xp_curve(levels: List[int], exponent: float = 1.5) -> List[int]:
    """Transformation of level progression into exponential growth integers."""
    return [int(lvl ** exponent) for lvl in levels]

def batch_process_entities(entities: List[Dict[str, any]], action_func: callable) -> List[any]:
    """Functional pipeline application for game entity collections."""
    return [action_func(e) for e in entities if 'active' in e and e['active']]