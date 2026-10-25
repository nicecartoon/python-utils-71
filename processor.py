import time
from typing import Dict, Any, List, Generator, Tuple

class GameInputError(ValueError):
    """Raised when a malformed or out-of-bounds input packet is received."""
    pass

class CommandProcessor:
    """Processes and sanitizes player input streams in real-time gaming loops."""

    BOUNDS = {"x": (-1000.0, 1000.0), "y": (-1000.0, 1000.0), "cooldown": (0.0, 10.0)}
    ALLOWED_KEYS = {"MOVE", "ATTACK", "CAST_SPELL", "PING"}

    def __init__(self, max_ticks_behind: int = 5):
        self.max_ticks_behind = max_ticks_behind
        self.tick_count = 0

    def _validate_payload(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if command not in self.ALLOWED_KEYS:
            raise GameInputError(f"Unrecognized action code: {command}")
        
        clean = {}
        for key, val in data.items():
            if key in self.BOUNDS:
                min_v, max_v = self.BOUNDS[key]
                if not isinstance(val, (int, float)) or not (min_v <= val <= max_v):
                    raise GameInputError(f"Value for {key} out of bounds [{min_v}, {max_v}]: {val}")
            clean[key] = val
        return clean

    def consume_frame(self, raw_frame: Dict[str, Any]) -> Generator[Tuple[int, str, Dict[str, Any]], None, None]:
        self.tick_count += 1
        frame_tick = raw_frame.get("tick", self.tick_count)
        
        if abs(self.tick_count - frame_tick) > self.max_ticks_behind:
            raise GameInputError(f"Frame synchronization error at tick {frame_tick}")

        inputs = raw_frame.get("inputs", [])
        if not isinstance(inputs, list):
            raise GameInputError("Input payload must be a sequence")

        for entry in inputs:
            player_id = entry.get("player_id")
            cmd = entry.get("cmd")
            payload = entry.get("data", {})

            if not isinstance(player_id, int) or player_id <= 0:
                continue

            validated = self._validate_payload(cmd, payload)
            yield (player_id, cmd, validated)
