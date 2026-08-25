# python-utils-71

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

python-utils-71 is a focused collection of Python utilities for 2D game development. It provides practical tools for procedural generation and game loop management without external dependencies.

## Features
- Multi-octave Perlin noise generator for terrain and texture creation
- Optimized A* pathfinding with diagonal movement and early termination
- High-resolution timer and event scheduler for precise frame control
- Lightweight game state serializer with versioned JSON output

## Installation

```bash
pip install python-utils-71
```

For development installation:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -e .
```

## Basic Usage

```python
from python_utils_71 import perlin, AStar, GameTimer

# Generate terrain data
heightmap = perlin(width=64, height=64, octaves=4, seed=42)

# Find path through obstacles
pathfinder = AStar(grid)
path = pathfinder.find((2, 3), (18, 15))

# Schedule game events
timer = GameTimer()
timer.every(0.5, update_enemies)
```