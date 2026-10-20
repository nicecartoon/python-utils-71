# python-utils-71

A lightweight collection of Python utilities designed to streamline gaming development, API integrations, and asset management. This toolkit focuses on high-performance data parsing and memory-efficient automation for game engines and discord-based game clients.

## Features

*   **Steam Web API Wrapper**: Simplify user authentication, inventory fetching, and game status tracking with minimal boilerplate.
*   **Log Parser**: High-speed regex engine for analyzing `.log` files from Unreal Engine or Unity, perfect for debugging session crashes.
*   **Asset Hashing**: Quickly verify integrity of large game assets using optimized CRC32 and SHA-256 batch processing.
*   **Memory Controller**: Cross-platform memory access utilities for monitoring process performance metrics during live gameplay.

## Installation

Install the package via pip:

```bash
pip install python-utils-71
```

For development mode, clone the repository and run:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -e .
```

## Usage

Easily integrate the Steam API handler into your project to track player stats:

```python
from utils_71.steam import SteamClient

# Initialize client
client = SteamClient(api_key="YOUR_STEAM_API_KEY")

# Fetch recent game playtime
playtime = client.get_recent_playtime(steam_id="76561198012345678")
print(f"Total minutes played in last 2 weeks: {playtime}")
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.