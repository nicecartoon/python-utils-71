# python-utils-71

A lightweight collection of Python utilities designed to streamline gaming development and automated task processing. This toolkit provides high-performance helpers for memory management, API integration, and game data parsing.

## Features

*   **Memory Scanner:** Low-latency pointer chaining and byte-pattern searching for debugging game processes.
*   **Packet Parser:** Built-in decoders for common binary serialization formats used in real-time multiplayer networking.
*   **Config Hot-Reloader:** Thread-safe JSON/YAML configuration management that monitors files for updates without restarting your script.
*   **Input Emulator:** Platform-agnostic interface for injecting mouse and keyboard events into windowed game applications.

## Installation

Ensure you have Python 3.8+ installed. Install the package directly via pip:

```bash
pip install python-utils-71
```

For developers requiring the latest cutting-edge features, clone the repository and install from source:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -e .
```

## Usage

Here is a quick example of how to use the memory scanner to track a player's health variable in a game process:

```python
from pyutils71 import MemoryScanner

# Attach to the game process by name
scanner = MemoryScanner(process_name="game.exe")

# Define pattern for health (e.g., 4-byte integer)
health_address = scanner.find_pattern("89 05 ? ? ? ? 8B 46 08")

if health_address:
    current_health = scanner.read_int(health_address)
    print(f"Current Player Health: {current_health}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.