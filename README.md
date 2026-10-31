# python-utils-71

A lightweight collection of Python utilities designed to streamline game development workflows and automate repetitive data processing tasks. This toolkit simplifies common challenges such as asset batch-processing, custom binary serialization, and integration with popular game engine APIs.

## Features

*   **Asset Batch Processor:** Recursively compress textures and optimize sprite sheets to reduce build sizes without sacrificing visual fidelity.
*   **Binary Data Marshaller:** Fast, structure-aligned binary serialization for custom file formats, ideal for high-performance save systems.
*   **Loot Table Engine:** A robust, weight-based random generation utility supporting complex conditional drops and probability modifiers.
*   **Engine API Bridge:** Simplified wrappers for interacting with common game engine SDKs, minimizing boilerplate code for data synchronization.

## Installation

Install `python-utils-71` via pip:

```bash
pip install python-utils-71
```

For local development and testing, clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -r requirements.txt
```

## Usage

Below is a quick example of how to use the Loot Table engine to handle drop mechanics for your game:

```python
from utils_71.gaming import LootTable

# Define a loot table with weight-based probabilities
items = {
    "Health Potion": 50,
    "Iron Sword": 10,
    "Legendary Cape": 1
}

loot_engine = LootTable(items)

# Roll for a random drop
result = loot_engine.roll()
print(f"Player acquired: {result}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.