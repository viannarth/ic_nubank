from src.baseline.plot import plot_graphs
from src.utils.eval_answers import count_correct_answers
from src.utils.config import EXAMS, MODEL_NAMES
from src.utils.files import json_from_dict
from copy import copy
import os

def main() -> None:

    # Toggle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    test_numbers = EXAMS[exam]["test_numbers"]

    # Dictionary of the performance (number of correct answers per total number of
    # valid questions) of each model
    model_dict = {f'{model}': 0.0 for model in MODEL_NAMES}
    model_performances = {f'{test_number}': copy(model_dict) for test_number in test_numbers}
    model_performances['all'] = copy(model_dict)

    for model in MODEL_NAMES:
        for test_number in test_numbers:
            model_answers_path = "./src/baseline/model_answers/" + exam + "/" + model + "/test_" + test_number + "_answers.json"
            correct_answers, accuracy = count_correct_answers(exam, test_number, model_answers_path)
            model_performances[test_number][model] = accuracy
            model_performances['all'][model] += correct_answers

    total_valid_questions = EXAMS[exam]["total_valid_questions"]
    for model in MODEL_NAMES:
        model_performances['all'][model] /= total_valid_questions

    # Export model_performances as a file
    folder_path = "./src/baseline/reports/" + exam
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/model_performances.json"
    json_from_dict(file_path, model_performances)

    # Generate plots from the dictionary
    plot_graphs(exam, model_performances)

if __name__ == "__main__":
    main()