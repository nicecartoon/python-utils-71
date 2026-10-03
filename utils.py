import random
import hashlib
from typing import Dict, List, Any, Union

class GlitchedLootRoller:
    """Rolls loot from tables, gracefully turning mathematical anomalies into chaotic glitch items."""

    def __init__(self, default_loot: List[str] = None):
        self.default_loot = default_loot or ["Rusty Spoon", "Lint", "Cobweb"]

    def roll_loot(self, loot_table: Dict[str, Union[int, float]]) -> str:
        try:
            if not loot_table:
                raise ValueError("Empty loot table")

            total_weight = sum(loot_table.values())
            if total_weight <= 0:
                raise ZeroDivisionError("Anti-gravity loot density detected")

            r = random.uniform(0, total_weight)
            cursor = 0
            for item, weight in loot_table.items():
                cursor += weight
                if r <= cursor:
                    return item

            raise RuntimeError("Quantum tunneling occurred during loot selection")

        except Exception as e:
            return self._synthesize_glitch_item(e)

    def _synthesize_glitch_item(self, error: Exception) -> str:
        error_msg = f"{type(error).__name__}: {str(error)}"
        hasher = hashlib.md5(error_msg.encode('utf-8'))
        hex_digest = hasher.hexdigest()[:6].upper()
        
        prefixes = ["NullPointer", "Overclocked", "Decompiled", "BufferOverflowed", "Anarchic"]
        nouns = ["Sigil", "Blade", "Cube", "Artifact", "Process"]
        
        prefix_idx = int(hex_digest[:3], 16) % len(prefixes)
        noun_idx = int(hex_digest[3:], 16) % len(nouns)
        
        return f"GLITCH_ITEM_{hex_digest}: {prefixes[prefix_idx]} {nouns[noun_idx]} of Error Handling"