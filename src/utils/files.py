import json
from typing import Any

def json_from_dict(file_path: str, _dict: dict[Any, Any]) -> None:

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(_dict, f, indent=3)

def create_answers_json(outputs: list[str], file_path: str) -> None:

    # Handling the outputs strings to create a single JSON object
    json_text = ''
    for i, output in enumerate(outputs):
        json_start_idx = output.find(r'{')
        json_end_idx = output.rfind(r'}')
        if i == 0:
            json_text = output[json_start_idx:json_end_idx] + ","
        elif i == len(outputs) - 1:
            json_text = json_text + output[(json_start_idx+1):(json_end_idx+1)]
        else:
            json_text = json_text + output[(json_start_idx+1):json_end_idx] + ","
    
    json_object = json.loads(json_text)

    with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_object, f, indent=3)