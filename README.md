# python-utils-71

`python-utils-71` is a specialized Python toolkit designed to streamline common tasks in game development and live service operations. It provides high-performance utilities for processing binary game assets, interacting with regional game APIs, and managing local configuration caches.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Key Features

*   **Binary Parser Engine:** Efficiently unpacks and serializes custom game data formats (.dat/.pak) into readable JSON structures.
*   **Latency Optimizer:** Includes a low-level network probe to measure jitter and ping against game backend endpoints.
*   **Config Sync Manager:** Handles atomic read/write operations for local client settings, preventing corruption during abrupt game crashes.
*   **Asset Hash Validator:** Provides fast MD5/SHA256 integrity checking to ensure local game files match server-side manifests.

### Installation

Ensure you have Python 3.9+ installed. You can install the package directly via pip:

```bash
# Clone the repository
git clone https://github.com/Developer/python-utils-71.git
cd python-utils-71

# Install requirements
pip install -r requirements.txt

# Install as a local package
pip install .
```

### Usage

Below is a quick example of how to use the `AssetHashValidator` to verify your local game files before launching.

```python
from utils_71.integrity import AssetHashValidator

# Initialize validator with the game data directory
validator = AssetHashValidator(data_path="./game_data")

# Check integrity against a remote manifest
is_valid = validator.verify_manifest("server_manifest.json")

if is_valid:
    print("Files verified. Launching game...")
else:
    print("Corruption detected. Initiating repair protocol.")
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.