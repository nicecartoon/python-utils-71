import os
import functools

class GameResourceCleaner:
    def __init__(self, directory: str):
        self.directory = directory

    def __call__(self, extension: str):
        return self.purge(extension)

    def purge(self, ext: str) -> int:
        files = [f for f in os.listdir(self.directory) if f.endswith(ext)]
        for f in files:
            os.remove(os.path.join(self.directory, f))
        return len(files)

def memoize_game_state(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def sanitize_path(path: str) -> str:
    return os.path.normpath(path).replace('\\', '/')

def validate_game_directory(path: str) -> bool:
    if not os.path.exists(path):
        return False
    return os.access(path, os.W_OK)

class ResourceRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, key: str, value: any):
        self._registry[key] = value

    def get_all(self):
        return {**self._registry}

    def reset(self):
        self._registry.clear()