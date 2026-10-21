import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, List

logger = logging.getLogger("gaming_processor")

@dataclass(frozen=True)
class TelemetryFrame:
    player_id: str
    position: tuple[float, float, float]
    health: float
    stamina: float
    timestamp: float

class TelemetryProcessor:
    """Processes game telemetry events with state-reconstruction error handling."""

    def __init__(self, max_health: float = 100.0, world_bounds: tuple[float, float] = (-1000.0, 1000.0)):
        self.max_health = max_health
        self.world_bounds = world_bounds
        self.last_valid_state: Dict[str, TelemetryFrame] = {}

    def sanitize_frame(self, raw_data: Dict[str, Any]) -> TelemetryFrame:
        player_id = str(raw_data.get("player_id", "unknown_entity"))
        pos = raw_data.get("position", (0.0, 0.0, 0.0))
        cleaned_pos = self._recover_position(player_id, pos)
        hp = self._recover_stat(raw_data.get("health"), self.max_health, player_id, "health")
        stamina = self._recover_stat(raw_data.get("stamina"), 100.0, player_id, "stamina")
        ts = raw_data.get("timestamp", 0.0)

        if not isinstance(ts, (int, float)) or ts < 0:
            last = self.last_valid_state.get(player_id)
            ts = (last.timestamp + 0.016) if last else 0.0

        frame = TelemetryFrame(player_id, cleaned_pos, hp, stamina, float(ts))
        self.last_valid_state[player_id] = frame
        return frame

    def _recover_position(self, player_id: str, pos: Any) -> tuple[float, float, float]:
        try:
            x, y, z = map(float, pos)
            for val in (x, y, z):
                if math.isnan(val) or math.isinf(val):
                    raise ValueError("Non-finite coordinate detected")
                if not (self.world_bounds[0] <= val <= self.world_bounds[1]):
                    raise ValueError(f"Out of bounds coordinate: {val}")
            return (x, y, z)
        except (TypeError, ValueError, IndexError) as err:
            logger.warning(f"Malformed position payload for {player_id}: {err}")
            last = self.last_valid_state.get(player_id)
            return last.position if last else (0.0, 0.0, 0.0)

    def _recover_stat(self, val: Any, max_val: float, player_id: str, stat_name: str) -> float:
        try:
            num = float(val)
            if math.isnan(num) or math.isinf(num):
                raise ValueError(f"Invalid numeric stat for {stat_name}")
            return max(0.0, min(num, max_val))
        except (TypeError, ValueError) as err:
            logger.warning(f"Corrupt stat '{stat_name}' for {player_id}: {err}")
            last = self.last_valid_state.get(player_id)
            return getattr(last, stat_name) if last else max_val

    def process_batch(self, batch: List[Dict[str, Any]]) -> List[TelemetryFrame]:
        processed = []
        for raw in batch:
            try:
                processed.append(self.sanitize_frame(raw))
            except Exception as unhandled:
                logger.error(f"Catastrophic frame drop prevented: {unhandled}")
                continue
        return processed
