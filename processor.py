import collections
import math

class XPScaleOptimizer:
    def __init__(self, base_xp=100, exponent=1.5):
        self.base = base_xp
        self.exp = exponent
        self._memo = {}

    def calculate_level_requirements(self, max_level):
        levels = range(1, max_level + 1)
        return {lvl: int(self.base * (lvl ** self.exp)) for lvl in levels}

    def flatten_combat_stats(self, data_packet):
        flat_data = {}
        def recurse(d, prefix=''):
            for k, v in d.items():
                new_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    recurse(v, new_key)
                else:
                    flat_data[new_key] = v
        recurse(data_packet)
        return flat_data

    def balance_loot_drops(self, items, weights):
        pool = []
        for item, weight in zip(items, weights):
            pool.extend([item] * int(weight * 100))
        return collections.Counter(pool)

def process_game_state(state):
    optimizer = XPScaleOptimizer()
    stats = optimizer.flatten_combat_stats(state)
    avg_power = sum(stats.values()) / max(1, len(stats))
    return {
        'status': 'optimized',
        'power_index': math.ceil(avg_power),
        'payload_size': len(stats)
    }