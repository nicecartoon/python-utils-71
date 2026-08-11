import json
from typing import Any, Dict, List

class DataHandler:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def filter_data(self, key: str, value: Any) -> List[Dict[str, Any]]:
        return [item for item in self.data if item.get(key) == value]

    def to_json(self) -> str:
        return json.dumps(self.data, indent=4)

    def from_json(self, json_str: str) -> None:
        self.data = json.loads(json_str)

    def sort_data(self, key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        return sorted(self.data, key=lambda x: x[key], reverse=reverse)

# Example Usage:
if __name__ == '__main__':
    example_data = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    ]

    handler = DataHandler(example_data)
    filtered = handler.filter_data('age', 30)
    print('Filtered Data:', filtered)
    sorted_data = handler.sort_data('age')
    print('Sorted Data:', sorted_data)
    json_output = handler.to_json()
    print('JSON Output:', json_output)