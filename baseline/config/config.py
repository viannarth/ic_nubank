import yaml

file_path = "./config.yaml"

with open(file_path, "r", encoding='utf-8') as f:
    config_data = yaml.safe_load(f)

EXAMS: dict[str, list[str] | int] = config_data['exams']
MODEL_NAMES: list[str] = config_data['model_names']
MODELS: dict[str, list[str] | dict[str, str | int]] = config_data['models']
IGNORED_QUESTIONS: dict[str, dict[str, list[str]]] = config_data['ignored_questions']