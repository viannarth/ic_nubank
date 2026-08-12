from src.baseline.dataset import get_questions_answers, extract_questions, answers_to_csv, questions_to_csv
from src.baseline.config import EXAMS
from pypdf import PdfReader

def main() -> None:

    # Toggle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    pdf_path = "./data/dataset/raw/" + exam + "_questions.pdf"
    reader = PdfReader(pdf_path)
    pages = reader.pages

    test_numbers = EXAMS[exam]["test_numbers"]

    # test_pages_idx: dict[str, range] = get_test_pages_idx(pages, exam)

    # This block of code is temporary
    ## 
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
    ##

    for test_number in test_numbers:
        test_questions = extract_questions(pages, test_pages_idx[test_number])
        questions_to_csv(exam, test_number, test_questions)
        answers_list = get_questions_answers(pages, exam, test_number)
        answers_to_csv(exam, test_number, answers_list)

if __name__ == "__main__":
    main()