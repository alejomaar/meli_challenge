from pydantic import BaseModel, Field


class FeedbackOpenQuestion(BaseModel):
    score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Score between 0 and 1 indicating how good the answer is",
    )
    reason: str = Field(
        ...,
        description="Very short and encouraging explanation that highlights the strengths of the answer and gently explains the score."
    )
