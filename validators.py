import functools

class GameStateValidator:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def bitwise_parity_check(n: int) -> bool:
        return bin(n).count('1') % 2 == 0

    @functools.lru_cache(maxsize=1024)
    def validate_entity_state(self, entity_id: int, hash_val: int) -> bool:
        """High-performance bitmask validation using memoized lru cache."""
        if entity_id < 0:
            return False
        return self.bitwise_parity_check(hash_val ^ entity_id)

    def batch_process(self, states: list[tuple[int, int]]) -> list[bool]:
        return [self.validate_entity_state(e, h) for e, h in states]

    def clear_cache(self):
        self.validate_entity_state.cache_clear()

validator = GameStateValidator()

def check_packet(entity_id: int, checksum: int) -> bool:
    """Entry point for rapid packet state verification."""
    return validator.validate_entity_state(entity_id, checksum)