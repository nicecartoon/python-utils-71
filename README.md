# python-utils-71

`python-utils-71` is a robust collection of Python scripts designed to streamline common tasks in gaming development and server management. It provides optimized tools for data parsing, process monitoring, and asset handling tailored for high-performance game environments.

## Features

*   **Log Parser:** Efficiently aggregate and filter game server logs to identify latency spikes and player connection anomalies.
*   **Asset Compressor:** Automated pipeline for batch-compressing texture and sound files using industry-standard compression ratios to minimize build sizes.
*   **Player Database Sync:** Simplified ORM helpers for synchronizing local player data with remote PostgreSQL databases.
*   **Process Watchdog:** A lightweight monitor that auto-restarts unresponsive game instances and reports crash logs to a dedicated Discord webhook.

## Installation

You can install the requirements via `pip` directly from the repository:

```bash
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71
pip install -r requirements.txt
```

## Usage

The following example demonstrates how to initialize the process watchdog to monitor a game server executable:

```python
from utils.watchdog import GameWatchdog

# Initialize watchdog for server instance
monitor = GameWatchdog(executable="./bin/game_server.exe", port=7777)

# Start monitoring process
monitor.start(interval=5)
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.