import json

def get_answers(filename: str) -> dict[str, str]:

    with open(filename, 'r', encoding='utf-8') as f:
        answers:dict[str, str] = json.load(f)

    return answers

def count_correct_answers(exam: str, test_number: str, model_answers_path: str) -> tuple[int, float]:

    answers_path = "./src/data/dataset/" + exam + "/answers/test_" + test_number + "_answers.json"

    test_answers = get_answers(answers_path)
    model_answers = get_answers(model_answers_path)
    
    correct_count: int = 0
    for question_number, letter in test_answers.items():
        if model_answers[question_number] == letter:
            correct_count += 1

    accuracy: float = correct_count / len(test_answers)

    return correct_count, accuracy