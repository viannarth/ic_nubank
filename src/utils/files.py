import json
from typing import Any

def json_from_dict(file_path: str, _dict: dict[Any, Any]) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(_dict, f, indent=3)