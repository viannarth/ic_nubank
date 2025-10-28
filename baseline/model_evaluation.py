import csv
import json

IGNORED_QUESTIONS = {
    "cpa-10": {
        "01": ["24", "25", "41"],
        "02": ["28", "39", "41"],
        "03": [],
        "04": [],
        "05": ["30", "34"],
        "06": ["31"],
        "07": [],
        "08": ["24", "25"]
    },
    "ancord-aai": {
        "01": ["43"],
        "02": [],
        "03": ["39"],
        "04": ["43", "47", "49", "67"],
        "05": ["78"],
        "06": ["78"]
    }
}

def get_answers(exam: str, test_number: str, filename: str) -> dict[str, str]:

    answers: dict[str, str] = {}
    # Get answers from CSV file
    if filename.endswith('.csv'):
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            r = csv.reader(f)
            next(r) # Skip header
            for row in r:
                question_number = row[0]
                # Skip ignored questions
                if question_number not in IGNORED_QUESTIONS[exam][test_number]:
                    letter = row[1]
                    answers[question_number] = letter

    # Get answers from JSON file
    elif filename.endswith('.json'): 
        with open(filename, 'r', encoding='utf-8') as f:
            all_answers = json.load(f)
            for question_number, letter in all_answers.items():
                # Skip ignored questions
                if question_number not in IGNORED_QUESTIONS[exam][test_number]:
                    answers[question_number] = letter

    return answers


def count_correct_answers(exam: str, test_number: str, model: str) -> int:

    answers_path = "./dataset/answers/" + exam + "/test_" + test_number + "_answers.csv"
    model_answers_path = "./models_answers/" + exam + "/" + model + "/test_" + test_number + "_answers.json"

    test_answers = get_answers(exam, test_number, answers_path)
    model_answers = get_answers(exam, test_number, model_answers_path)
    
    correct_count: int = 0
    for question_number, letter in test_answers.items():
        if model_answers[question_number] == letter:
            correct_count += 1

    return correct_count