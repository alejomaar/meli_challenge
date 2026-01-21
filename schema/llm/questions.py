from typing import List, Literal, Union

from pydantic import BaseModel, Field, model_validator


class Option(BaseModel):
    text: str
    is_correct: bool


class OpenQuestion(BaseModel):
    description: str


class ClosedQuestion(BaseModel):
    description: str
    options: List[Option] = Field(min_length=2, max_length=4)

    @model_validator(mode="after")
    def validate_single_correct(self):
        if sum(o.is_correct for o in self.options) != 1:
            raise ValueError("Exactly one option must be correct")
        return self


class QuestionsStructuredOutput(BaseModel):
    questions: List[OpenQuestion| ClosedQuestion] = Field(min_length=2, max_length=3)
