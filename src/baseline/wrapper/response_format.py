from src.utils.config import EXAMS
from typing import Type, Literal, Any
from pydantic import BaseModel, ConfigDict, create_model

# TODO: skip ignored questions
# TODO: separate baseline response format from RAG response format
def generate_json_schemas(exam: str) -> list[dict[str, Any]]:

    questions_per_exam = EXAMS[exam]["questions_per_exam"]
    chunk_size = EXAMS[exam]["chunk_size"]

    answers_schema = { "$ref": "#/$defs/Answers" }
    response_schemas = []

    for first_question_idx in range(0, questions_per_exam, chunk_size):
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

        response_schemas.append(response_format)

    return response_schemas

def generate_response_models(exam: str) -> list[Type[BaseModel]]:
    questions_per_exam = EXAMS[exam]["questions_per_exam"]
    chunk_size = EXAMS[exam]["chunk_size"]

    response_models: list[Type[BaseModel]] = []

    for first_question_idx in range(0, questions_per_exam, chunk_size):
        field_definitions = {}

        for j in range(1, chunk_size + 1):
            question_number = f"{(j + first_question_idx):02d}" 

            field_definitions[question_number] = (Literal["a", "b", "c", "d"])

        model = create_model(
            "QuestionAnswers",
            __config__=ConfigDict(extra="forbid"),
            **field_definitions
        )

        response_models.append(model)

    return response_models