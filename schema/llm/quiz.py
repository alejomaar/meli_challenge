from typing import List

from pydantic import BaseModel, Field, conint


class Option(BaseModel):
    id: conint(ge=1) = Field(..., description="1-based option id")
    description: str = Field(..., min_length=1)


class QuizItem(BaseModel):
    question: str = Field(..., min_length=1)
    options: List[Option] = Field(..., min_length=2)
    right_option: conint(ge=1) = Field(..., description="Must match one of the option ids")
