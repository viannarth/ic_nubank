from src.utils.config import EXAMS, IGNORED_QUESTIONS
from typing import Any

def generate_json_schemas(exam: str, test_number: str) -> list[dict[str, Any]]:

    questions_per_exam = EXAMS[exam]["questions_per_exam"]
    chunk_size = EXAMS[exam]["chunk_size"]

    answers_schema = { "$ref": "#/$defs/Answers" }
    response_schemas = []

    for first_question_idx in range(0, questions_per_exam, chunk_size):
        properties = {f"{(j + first_question_idx):02d}": answers_schema for j in range(1, chunk_size + 1) if j not in IGNORED_QUESTIONS[exam][test_number]}
        required = [f"{(j + first_question_idx):02d}" for j in range (1, chunk_size + 1) if j not in IGNORED_QUESTIONS[exam][test_number]]

        json_schema = {
            "$defs": {
                "Answers": {
                    "enum": [
                        "a",
                        "b",
                        "c",
                        "d"
                    ],
                    "title": "Answers",
                    "type": "string"
                }
            },
            "properties": properties,
            "required": required,
            "additionalProperties": False,
            "title": "QuestionAnswers",
            "type": "object"
        }

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "QuestionAnswer",
                "description": "JSON schema for the format of the answers of the questions.",
                "schema": json_schema,
                "strict": True
            }
        }

        response_schemas.append(response_format)

    return response_schemas