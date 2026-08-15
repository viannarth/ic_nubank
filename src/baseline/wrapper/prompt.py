from src.utils.config import EXAMS, IGNORED_QUESTIONS
import json
import random

def generate_prompts(exam: str, test_number: str) -> list[str]:

    questions_per_exam = EXAMS[exam]["questions_per_exam"]
    chunk_size = EXAMS[exam]["chunk_size"]

    base_prompt_path = "./src/baseline/wrapper/base_prompt.txt"
    questions_path = "./src/data/dataset/" + exam + "/questions/test_" + test_number + "_questions.csv"

    with open(base_prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()

    EXAM_PROMPTS = {
        "ancord-aai": "ANCORD (Associação Nacional das Corretoras e Distribuidoras de Títulos e Valores Mobiliários, Câmbio e Mercadorias) Investment Advisor",
        "cpa-10": "CPA-10 (Certificação Profissional ANBIMA Série 10)"
    }

    exam_prompt = EXAM_PROMPTS[exam]
    base_prompt = base_prompt.replace("{EXAM}", exam_prompt)

    with open(questions_path, 'r', encoding='utf-8') as f:
        questions = f.read()
    
    lines = questions.strip().splitlines()
    header = lines[0]

    alternatives = ['a', 'b', 'c', 'd']
    questions_sentence = "[QUESTIONS_CSV_BEGIN]"
    chunks = []
    for first_question_idx in range(0, questions_per_exam, chunk_size):
        start = first_question_idx + 1
        end = first_question_idx + chunk_size + 1

        dict_example = {f"{(j + first_question_idx):02d}": random.choice(alternatives) for j in range(1, chunk_size + 1) if j not in IGNORED_QUESTIONS[exam][test_number]}
        json_example = json.dumps(dict_example) + '\n'

        chunk = lines[start:end]
        chunk = [json_example, questions_sentence, header] + chunk
        chunk = "\n".join(chunk) # Transforms the list of lines to a string

        chunks.append(chunk)

    prompts = []
    for chunk in chunks:
        prompt = base_prompt + chunk
        prompts.append(prompt)

    return prompts