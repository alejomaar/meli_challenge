from typing import List

from pydantic import BaseModel


class FeedbackAnswerItem(BaseModel):
    """Feedback generated for a single answer."""
    assessment_id: int
    answer_id: int
    score: float
    feedback: str


class CreateAssessmentFeedbackResponse(BaseModel):
    """Feedback results for an assessment."""
    results: List[FeedbackAnswerItem]
