from pathlib import Path

def generate_prompts(exam: str, test_number: str) -> dict[str, str]:

    base_prompt_path = "./src/rag/base_prompt.txt"
    base_prompt = Path(base_prompt_path).read_text(encoding="utf-8")

    questions_path = "./src/data/dataset/" + exam + "/questions/test_" + test_number + "_questions.csv"
    questions = Path(questions_path).read_text(encoding="utf-8")
    question_lines = questions.strip().splitlines()
    header = question_lines[0]

    exam_names = {
        "ancord-aai": "ANCORD Investment Advisor",
        "cpa-10": "ANBIMA CPA-10"
    }

    exam_placeholder = exam_names[exam]
    base_prompt = base_prompt.replace("{EXAM}", exam_placeholder)

    prompts:dict[str, str] = {}

    for idx in range(1, len(question_lines)):
        question = question_lines[idx]

        question_number = question[1:3]

        prompt = "\n".join([base_prompt, header, question])

        prompts[question_number] = prompt

    return prompts