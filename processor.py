import random
from typing import List, Any, Dict

class AliasTableProcessor:
    """
    Fast O(1) weighted random selection processor for gaming loot tables
    and probability-based spawn systems using Vose's Alias Method.
    """
    def __init__(self, items_with_weights: Dict[Any, float]):
        if not items_with_weights:
            raise ValueError("Loot table cannot be empty")
        
        self.items = list(items_with_weights.keys())
        weights = list(items_with_weights.values())
        total_weight = float(sum(weights))
        
        if total_weight <= 0:
            raise ValueError("Total weight must be positive")
            
        n = len(weights)
        self.prob = [0.0] * n
        self.alias = [0] * n
        
        scaled_prob = [w * n / total_weight for w in weights]
        small = [i for i, p in enumerate(scaled_prob) if p < 1.0]
        large = [i for i, p in enumerate(scaled_prob) if p >= 1.0]
        
        while small and large:
            less = small.pop()
            more = large.pop()
            
            self.prob[less] = scaled_prob[less]
            self.alias[less] = more
            
            scaled_prob[more] = (scaled_prob[more] + scaled_prob[less]) - 1.0
            if scaled_prob[more] < 1.0:
                small.append(more)
            else:
                large.append(more)
                
        while large:
            self.prob[large.pop()] = 1.0
        while small:
            self.prob[small.pop()] = 1.0

    def sample(self) -> Any:
        """Sample a single item in O(1) time complexity."""
        n = len(self.items)
        idx = random.randint(0, n - 1)
        if random.random() < self.prob[idx]:
            return self.items[idx]
        return self.items[self.alias[idx]]

    def sample_batch(self, count: int) -> List[Any]:
        """Generates a batch of drops from the loot table."""
        return [self.sample() for _ in range(count)]


def process_drop_rates(loot_table: Dict[str, float], rolls: int = 1) -> Dict[str, int]:
    """Utility function to simulate loot table roll results over multiple attempts."""
    processor = AliasTableProcessor(loot_table)
    results: Dict[str, int] = {}
    for item in processor.sample_batch(rolls):
        results[item] = results.get(item, 0) + 1
    return results
