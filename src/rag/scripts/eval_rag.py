from src.utils.eval_answers import count_correct_answers
from src.utils.config import EXAMS
from src.utils.files import json_from_dict
import os

def main() -> None:

    # Toggle the exam
    # exam = "ancord-aai"
    exam = "cpa-10"

    test_numbers = EXAMS[exam]["test_numbers"]

    rag_performance:dict[str, float] = {f"{test_number}": 0.0 for test_number in test_numbers}
    rag_performance["all"] = 0.0

    for test_number in test_numbers:
        model_answers_path = "./src/rag/answers/" + exam + "/test_" + test_number + "_answers.json"
        correct_answers, accuracy = count_correct_answers(exam, test_number, model_answers_path)
        rag_performance[test_number] = accuracy
        rag_performance["all"] += correct_answers

    total_valid_questions = EXAMS[exam]["total_valid_questions"]
    rag_performance['all'] /= total_valid_questions

    # Export rag_performance as a file
    folder_path = "./src/rag/reports/" + exam
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/rag_performance.json"
    json_from_dict(file_path, rag_performance)

if __name__ == "__main__":
    main()