from pypdf import PageObject
import re
import csv
import os

def get_questions_answers(pages: list[PageObject], exam: str, test_number: str) -> dict[str, str]:

    EXAM_ANSWERS_HEADERS: dict[str, str] = {
        "ancord-aai": rf"ANCORD:\sSIMULADO",
        "cpa-10": rf"CPA10-SIMULADO"
    }

    exam_answers_header = EXAM_ANSWERS_HEADERS[exam]

    answers_page = pages[-1].extract_text()

    # Regular expression for the pattern of the header of the test answers
    test_pattern = re.compile(
        rf"{exam_answers_header}\s\({test_number}\)(.*?)(?={exam_answers_header}|\Z)",
        re.DOTALL
    )

    test_answers = test_pattern.search(answers_page).group(1)

    question_pattern = re.compile(r"\d+[.]\s[A-Z]")

    matches = re.findall(question_pattern, test_answers)

    answers = {}

    for match in matches:
        split = match.split()
        question_number = split[0].replace('.', '')
        letter = split[1].lower()
        answers[question_number] = letter
    
    return answers


# TODO: implement to automatically get the index of the pages of each test
def get_test_pages_idx(pages: list[PageObject], exam: str) -> dict[str, range]:

    pass


def extract_questions(pages: list[PageObject], test_pages_idx: range) -> list[dict[str, str]]:

    questions: list[dict[str, str]] = []

    # Extract the questions of one test
    for idx in test_pages_idx:
        page = pages[idx]
        text = page.extract_text()
        text = text[:-2] # Remove page number

        # Regular expression to identify the question format in the page text
        question_pattern = re.compile(
            r"(\d{2})\s+[[]\w+[\w-]*[]]\s+(.*?)\s*a\)\s(.*?)\s*b\)\s(.*?)\s*c\)\s(.*?)\s*d\)\s(.*?)(?=\d{2}\s+\[|$)",
            re.DOTALL
        )

        matches = question_pattern.findall(text) # Returns a tuple of matches (questions)
        for match in matches:

            # Post-processing the texts of each attribute
            def post_process_string(attr: str) -> str:
                new_attr = re.sub(r'\s+', ' ', attr).strip() # Remove the newlines and extra space characters
                banned_chars = ["ª", "º", "/"]
                # Remove special characters
                for char in banned_chars:
                    new_attr = new_attr.replace(char, '')

                ligatures = {
                    "ﬀ": "ff",
                    "ﬁ": "fi",
                    "ﬂ": "fl",
                    "ﬃ": "ffi",
                    "ﬄ": "ffl",
                    "ﬅ": "ft",
                    "ﬆ": "st",
                    "Ꜳ": "AA",
                    "Æ": "AE",
                    "ꜳ": "aa",
                }
                # Ligatures replacement
                for search, replace in ligatures.items():
                    new_attr = new_attr.replace(search, replace)
                
                return new_attr

            question_number: str = match[0]

            question = {
                "number": question_number,
                "statement": post_process_string(match[1]),
                "a": post_process_string(match[2]),
                "b": post_process_string(match[3]),
                "c": post_process_string(match[4]),
                "d": post_process_string(match[5]),
            }

            post_process_string(match[1])

            questions.append(question)

    return questions

# TODO: remove this function
def answers_to_csv(exam: str, test_number: str, answers_list: dict[str, str]) -> None:

    fieldnames = ["number", "answer"]

    folder_path = "./src/data/dataset/" + exam + "/answers"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/test_" + test_number + "_answers.csv"
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(fieldnames)
        w.writerows(answers_list.items())


def questions_to_csv(exam: str, test_number: str, questions_list: list[dict[str, str]]) -> None:

    fieldnames = list(questions_list[0].keys())

    folder_path = "./src/data/dataset/" + exam + "/questions"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/test_" + test_number + "_questions.csv"
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(questions_list)