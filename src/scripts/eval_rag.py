from src.baseline.model_evaluation import count_correct_answers
from src.baseline.config import EXAMS, IGNORED_QUESTIONS
import os
import json

def main()->None:

    # Toggle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"
    model = "rag"

    test_numbers = EXAMS[exam]["test_numbers"]

    # List of the number of not ignored questions for each test of the exam
    test_valid_questions = [EXAMS[exam]["total_number_questions"] - len(ignored_test_questions) for ignored_test_questions in IGNORED_QUESTIONS[exam].values()]

    rag_performance:dict[str, float] = {f"{test_number}": 0.0 for test_number in test_numbers}
    rag_performance["all"] = 0.0

    for test_number, number_valid_questions in zip(test_numbers, test_valid_questions):
        correct_answers = count_correct_answers(exam, test_number, model)
        rag_performance[test_number] = correct_answers / number_valid_questions
        rag_performance["all"] += correct_answers

    rag_performance['all'] /= sum(test_valid_questions)

    # Export model_performances as a file
    folder_path = "./reports/" + exam
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/rag_performance.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(rag_performance, f, indent=4)

if __name__ == "__main__":
    main()