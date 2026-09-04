# python-utils-71

`python-utils-71` is a robust Python toolkit designed to streamline game development workflows, focusing on memory management and high-frequency data processing. This library provides optimized utilities to handle asset caching, game state serialization, and low-latency input polling for Python-based game engines.

## Features

*   **Async Asset Loader:** Thread-safe resource manager that handles background loading of textures and audio files to prevent main-thread stutter.
*   **Game State Compressor:** Efficient binary serialization utility for saving complex game sessions with minimal disk footprint.
*   **Delta-Time Smoothing:** High-precision timing utilities to stabilize physics updates regardless of frame rate fluctuations.
*   **Key-Combo Mapper:** Advanced input handling middleware for complex macro creation and rebindable control schemes.

## Installation

Install the package via pip:

```bash
pip install python-utils-71
```

For development mode and access to build tools:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -e .
```

## Basic Usage

Quickly implement the asset caching system to manage your game resources:

```python
from utils_71.assets import AssetManager

# Initialize the manager
manager = AssetManager(cache_size=128)

# Load resources asynchronously
manager.load("assets/textures/player_ship.png")

# Retrieve resource
sprite = manager.get("player_ship")

# Verify cache health
print(f"Current cache hit rate: {manager.get_hit_rate()}%")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.