import math
import time
from typing import Any, Callable, Generator

VALIDATORS: dict[str, Callable[[dict[str, Any]], bool]] = {
    "move": lambda p: (
        isinstance(p.get("x"), (int, float))
        and isinstance(p.get("y"), (int, float))
        and math.hypot(p["x"], p["y"]) <= 1000.0
    ),
    "cast_spell": lambda p: (
        isinstance(p.get("spell_id"), int)
        and 1 <= p["spell_id"] <= 255
        and isinstance(p.get("mana_cost"), int)
        and p["mana_cost"] >= 0
    ),
    "chat": lambda p: (
        isinstance(p.get("message"), str)
        and 0 < len(p["message"]) <= 128
        and not any(bad in p["message"].lower() for bad in ["<script>", "drop table"])
    ),
}

def process_input_stream(raw_inputs: list[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    now = time.time()
    for frame in raw_inputs:
        match frame:
            case {"cmd": str(cmd), "payload": dict(payload), "timestamp": float(ts)} if abs(now - ts) <= 5.0:
                validator = VALIDATORS.get(cmd)
                if not validator:
                    continue
                if not validator(payload):
                    continue
                yield {"cmd": cmd, "data": payload, "status": "VALIDATED", "processed_at": now}
            case {"cmd": str(cmd), "timestamp": ts} if not isinstance(ts, (int, float)):
                continue
            case _:
                continue

if __name__ == "__main__":
    sample_frames = [
        {"cmd": "move", "payload": {"x": 10.5, "y": 20.0}, "timestamp": time.time()},
        {"cmd": "cast_spell", "payload": {"spell_id": 42, "mana_cost": 15}, "timestamp": time.time()},
        {"cmd": "chat", "payload": {"message": "gg wp!"}, "timestamp": time.time()},
        {"cmd": "move", "payload": {"x": 99999.0, "y": 0.0}, "timestamp": time.time()},
    ]
    results = list(process_input_stream(sample_frames))
    print(f"Processed {len(results)} valid input frames.")
