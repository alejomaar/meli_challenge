from typing import List

from pydantic import BaseModel, Field, model_validator


class Option(BaseModel):
    """Single option for a closed (multiple-choice) question."""
    text: str
    is_correct: bool


class OpenQuestion(BaseModel):
    """Open-ended survey question."""
    description: str


class ClosedQuestion(BaseModel):
    """Multiple-choice question with a guided explanation."""
    description: str
    hint: str = Field(
        ...,
        description="Guided explanation revealing the correct answer and why other choices are incorrect.",
    )
    options: List[Option] = Field(min_length=2, max_length=4)

    @model_validator(mode="after")
    def validate_single_correct(self):
        if sum(o.is_correct for o in self.options) != 1:
            raise ValueError("Exactly one option must be correct")
        return self


class QuestionsStructuredOutput(BaseModel):
    """Structured output containing generated survey questions."""
    open_questions: list[OpenQuestion] = Field(min_length=2, max_length=3)
    closed_questions: list[ClosedQuestion] = Field(min_length=2, max_length=3)
