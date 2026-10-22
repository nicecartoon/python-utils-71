import time
import threading
from typing import Callable, Dict

class GameSessionManager:
    def __init__(self):
        self._tasks: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._active = True

    def register_task(self, name: str, func: Callable):
        with self._lock:
            self._tasks[name] = func

    def execute_tick(self):
        for name, task in self._tasks.items():
            try:
                task()
            except Exception as e:
                print(f"Task {name} failed: {e}")

    def shutdown(self):
        self._active = False
        self._tasks.clear()

class EntityRegistry:
    def __init__(self):
        self._registry = {}

    def __setitem__(self, key, value):
        self._registry[key] = value

    def __getitem__(self, key):
        return self._registry.get(key)

def initialize_engine():
    session = GameSessionManager()
    registry = EntityRegistry()
    return session, registry

if __name__ == "__main__":
    session, registry = initialize_engine()
    session.register_task("heartbeat", lambda: print(f"Tick at {time.time()}"))
    session.execute_tick()