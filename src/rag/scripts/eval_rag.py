from src.utils.eval_answers import count_correct_answers
from src.utils.config import EXAMS, IGNORED_QUESTIONS
from src.utils.files import json_from_dict
import os

def main() -> None:

    # Toggle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    # TODO: remove this model logic
    model = "rag"

    test_numbers = EXAMS[exam]["test_numbers"]

    # TODO: transfer this boilerplate to utils folder
    # List of the number of not ignored questions for each test of the exam
    test_valid_questions = [EXAMS[exam]["total_number_questions"] - len(ignored_test_questions) for ignored_test_questions in IGNORED_QUESTIONS[exam].values()]

    rag_performance:dict[str, float] = {f"{test_number}": 0.0 for test_number in test_numbers}
    rag_performance["all"] = 0.0

    for test_number, number_valid_questions in zip(test_numbers, test_valid_questions):
        correct_answers = count_correct_answers(exam, test_number, model)
        rag_performance[test_number] = correct_answers / number_valid_questions
        rag_performance["all"] += correct_answers

    rag_performance['all'] /= sum(test_valid_questions)

    # Export rag_performance as a file
    folder_path = "./src/rag/reports/" + exam
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/rag_performance.json"
    json_from_dict(file_path, rag_performance)

if __name__ == "__main__":
    main()