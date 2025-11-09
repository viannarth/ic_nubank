import yaml

file_path = "./baseline/config/config.yaml"

with open(file_path, "r", encoding='utf-8') as f:
    config_data = yaml.safe_load(f)

EXAMS = config_data['exams']
MODEL_NAMES = config_data['model_names']
MODELS = config_data['models']
IGNORED_QUESTIONS = config_data['ignored_questions']