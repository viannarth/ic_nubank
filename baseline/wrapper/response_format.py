from typing import Any

def generate_response_formats(total_number_questions: int, chunk_size: int) -> list[dict[str, Any]]:

    answers_schema = { "$ref": "#/$defs/Answers" }
    response_formats = []

    for first_question_idx in range(0, total_number_questions, chunk_size):
        properties = {f"{(j + first_question_idx):02d}": answers_schema for j in range(1, chunk_size + 1)}
        required = [f"{(j + first_question_idx):02d}" for j in range (1, chunk_size + 1)]

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

        response_formats.append(response_format)

    return response_formats