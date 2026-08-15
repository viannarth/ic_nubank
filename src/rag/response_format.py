from src.utils.config import EXAMS, IGNORED_QUESTIONS
from typing import Type, Literal
from pydantic import BaseModel, ConfigDict, create_model

def generate_response_models(exam: str, test_number: str) -> list[Type[BaseModel]]:
    questions_per_exam = EXAMS[exam]["questions_per_exam"]
    chunk_size = EXAMS[exam]["chunk_size"]

    response_models: list[Type[BaseModel]] = []

    for first_question_idx in range(0, questions_per_exam, chunk_size):
        field_definitions = {}

        for j in range(1, chunk_size + 1):
            # Skip ignored questions
            if j in IGNORED_QUESTIONS[exam][test_number]:
                continue
        
            question_number = f"{(j + first_question_idx):02d}" 

            field_definitions[question_number] = (Literal["a", "b", "c", "d"])

        model = create_model(
            "QuestionAnswers",
            __config__=ConfigDict(extra="forbid"),
            **field_definitions
        )

        response_models.append(model)

    return response_models