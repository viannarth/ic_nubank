from typing import Literal
from pydantic import BaseModel, ConfigDict

class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: Literal["a", "b", "c", "d"]

def json_from_answer(response: str, question_number: str) -> str:

    return response.replace("answer", question_number)