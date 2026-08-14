from src.data.dataset import get_questions_answers, extract_questions, questions_to_csv
from src.utils.config import EXAMS
from src.utils.files import json_from_dict
from pypdf import PdfReader
import os

def main() -> None:

    # Toggle the exam
    # exam = "cpa-10"
    exam = "ancord-aai"

    pdf_path = "./src/data/dataset/raw/" + exam + "_questions.pdf"
    reader = PdfReader(pdf_path)
    pages = reader.pages

    test_numbers = EXAMS[exam]["test_numbers"]

    # Toogle the test pages indexes
    # CPA-10
    # test_pages_idx: dict[str, range] = {
    #     "01": range(3, 15), 
    #     "02": range(15, 27), 
    #     "03": range(27, 39), 
    #     "04": range(39, 50),
    #     "05": range(50, 62), 
    #     "06": range(62, 74), 
    #     "07": range(74, 85), 
    #     "08": range(85, 97)
    # }

    # Ancord AAI
    test_pages_idx: dict[str, range] = {
        "01": range(3, 22), 
        "02": range(22, 42), 
        "03": range(42, 61), 
        "04": range(61, 80),
        "05": range(80, 99), 
        "06": range(99, 117)
    }

    for test_number in test_numbers:
        test_questions = extract_questions(pages, exam, test_number, test_pages_idx[test_number])
        questions_to_csv(exam, test_number, test_questions)

        answers_list = get_questions_answers(pages, exam, test_number)

        folder_path = "./src/data/dataset/" + exam + "/answers"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = folder_path + "/test_" + test_number + "_answers.json"

        json_from_dict(file_path, answers_list)

if __name__ == "__main__":
    main()