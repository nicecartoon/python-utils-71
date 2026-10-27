import time
from typing import Callable, Any, Dict, List
from collections import deque

class FramePipeline:
    """A creative game event processor executing queued frame actions with delta-time binding."""
    
    def __init__(self, target_fps: int = 60):
        self.fps = target_fps
        self.frame_time = 1.0 / target_fps
        self._hooks: Dict[str, List[Callable[[float], Any]]] = {"pre": [], "main": [], "post": []}
        self._history: deque = deque(maxlen=target_fps * 5)
        self._last_tick = time.perf_counter()

    def __getitem__(self, stage: str) -> List[Callable[[float], Any]]:
        if stage not in self._hooks:
            self._hooks[stage] = []
        return self._hooks[stage]

    def register(self, stage: str = "main"):
        def decorator(func: Callable[[float], Any]):
            self[stage].append(func)
            return func
        return decorator

    def tick(self, forced_dt: float | None = None) -> Dict[str, int]:
        now = time.perf_counter()
        dt = forced_dt if forced_dt is not None else (now - self._last_tick)
        dt = max(dt, 0.001)
        self._last_tick = now

        executed = {"pre": 0, "main": 0, "post": 0}
        for phase in ("pre", "main", "post"):
            for callback in self._hooks.get(phase, []):
                callback(dt)
                executed[phase] += 1

        self._history.append((now, sum(executed.values())))
        return executed

    @property
    def average_throughput(self) -> float:
        if len(self._history) < 2:
            return 0.0
        total_ops = sum(ops for _, ops in self._history)
        time_span = max(self._history[-1][0] - self._history[0][0], 0.001)
        return round(total_ops / time_span, 2)
