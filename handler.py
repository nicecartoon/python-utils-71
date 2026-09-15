import sys
import math
from typing import Any, Dict, Tuple

class GamingInputHandler:
    """Handles chaotic, drifted, or corrupted game inputs with extreme resilience."""

    VALID_COMMANDS = {"move", "jump", "shoot", "reload", "pause"}

    def __init__(self, deadzone: float = 0.15, max_magnitude: float = 1.0):
        self.deadzone = deadzone
        self.max_magnitude = max_magnitude

    def resolve_vector(self, x: Any, y: Any) -> Tuple[float, float]:
        """Sanitizes raw joystick inputs, mitigating hardware drift and magnitude overflows."""
        def _clean(val: Any) -> float:
            try:
                num = float(val)
                if math.isnan(num) or math.isinf(num):
                    return 0.0
                return math.copysign(min(abs(num), self.max_magnitude), num)
            except (ValueError, TypeError):
                return 0.0

        cx, cy = _clean(x), _clean(y)
        magnitude = math.hypot(cx, cy)
        if magnitude < self.deadzone:
            return 0.0, 0.0
        if magnitude > self.max_magnitude:
            scale = self.max_magnitude / magnitude
            return cx * scale, cy * scale
        return cx, cy

    def decode_command(self, payload: Any) -> Dict[str, Any]:
        """Extracts actionable commands even from corrupt, nested, or misspelled events."""
        result = {"command": "idle", "params": {}}
        if not payload:
            return result

        while isinstance(payload, (list, tuple)) and len(payload) > 0:
            payload = payload[0]

        if isinstance(payload, dict):
            cmd = str(payload.get("cmd", payload.get("action", ""))).lower().strip()
            coords = payload.get("coords", (0.0, 0.0))
        else:
            cmd = str(payload).lower().strip()
            coords = (0.0, 0.0)

        matched = "idle"
        for valid in self.VALID_COMMANDS:
            if valid in cmd or cmd in valid:
                matched = valid
                break

        if matched == "move":
            if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                x, y = self.resolve_vector(coords[0], coords[1])
            else:
                x, y = 0.0, 0.0
            result["params"] = {"x": x, "y": y}

        result["command"] = matched
        return result