from typing import Dict, List, Tuple, Optional

class ComboProcessor:
    """Processes fighting game directional inputs using complex vector representation.

    Translates standard numpad notations (e.g., '236' for Quarter Circle Forward)
    into 2D vector paths modeled as complex numbers, offering a novel way
    to perform sub-sequence matching for special moves.
    """

    COMPLEX_DIRECTIONS: Dict[str, complex] = {
        "1": -1.0 - 1.0j, "2": -1.0j,       "3": 1.0 - 1.0j,
        "4": -1.0,        "5": 0.0 + 0.0j,  "6": 1.0,
        "7": -1.0 + 1.0j, "8": 1.0j,        "9": 1.0 + 1.0j
    }

    def __init__(self) -> None:
        """Initializes an empty input buffer and a move registration registry."""
        self.buffer: List[complex] = []
        self.registry: Dict[Tuple[complex, ...], str] = {}

    def register_move(self, pattern: str, move_name: str) -> None:
        """Registers a move sequence using standard numpad notation string.

        Args:
            pattern: A sequence of digits (e.g., '236' for fireball).
            move_name: The name of the triggered action.
        """
        vector_seq: Tuple[complex, ...] = tuple(
            self.COMPLEX_DIRECTIONS[char] for char in pattern if char in self.COMPLEX_DIRECTIONS
        )
        if vector_seq:
            self.registry[vector_seq] = move_name

    def receive_input(self, direction_key: str) -> Optional[str]:
        """Appends an input key to the buffer and checks if any move triggers.

        Args:
            direction_key: A string key from '1' to '9'.

        Returns:
            The name of the detected move if triggered, otherwise None.
        """
        if direction_key not in self.COMPLEX_DIRECTIONS:
            return None

        self.buffer.append(self.COMPLEX_DIRECTIONS[direction_key])

        max_len = max((len(seq) for seq in self.registry.keys()), default=0)
        if len(self.buffer) > max_len * 2:
            self.buffer.pop(0)

        for seq, name in sorted(self.registry.items(), key=lambda item: len(item[0]), reverse=True):
            if len(self.buffer) >= len(seq):
                if tuple(self.buffer[-len(seq):]) == seq:
                    self.buffer.clear()
                    return name
        return None