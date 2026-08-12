from src.baseline.model_evaluation import count_correct_answers
from src.baseline.plots import plot_graphs
from src.baseline.config import EXAMS, MODEL_NAMES, IGNORED_QUESTIONS
from copy import copy
import os
import json

def main() -> None:

    # Toggle the exam
    # exam = "ancord-aai"
    exam = "cpa-10"

    test_numbers = EXAMS[exam]["test_numbers"]

    # Dictionary of the performance (number of correct answers per total number of
    # valid questions) of each model
    model_dict = {f'{model}': 0.0 for model in MODEL_NAMES}
    model_performances = {f'{test_number}': copy(model_dict) for test_number in test_numbers}
    model_performances['all'] = copy(model_dict)

    # List of the number of not ignored questions for each test of the exam
    test_valid_questions = [EXAMS[exam]["total_number_questions"] - len(ignored_test_questions) for ignored_test_questions in IGNORED_QUESTIONS[exam].values()]

    for test_number, number_valid_questions in zip(test_numbers, test_valid_questions):
        for model in MODEL_NAMES:
            correct_answers = count_correct_answers(exam, test_number, model)
            model_performances[test_number][model] = correct_answers / number_valid_questions
            model_performances['all'][model] += correct_answers
    
    for model in MODEL_NAMES:
        model_performances['all'][model] /= sum(test_valid_questions)

    # Export model_performances as a file
    folder_path = "./reports/" + exam
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/model_performances.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(model_performances, f, indent=4)

    plot_graphs(exam, model_performances)

if __name__ == "__main__":
    main()