from typing import Optional

from pydantic import BaseModel


class SurveyAnswers(BaseModel):
    """Single answer to a survey question."""
    question_id: int
    selected_option_id: Optional[int] = None
    text_answer: Optional[str] = None


class SurveyAnswersPayload(BaseModel):
    """Payload containing all answers for a survey submission."""
    answers: list[SurveyAnswers]


class CreateSurveyPayload(BaseModel):
    """create survey payload."""

    topic: str


class CreateSurveyResponse(BaseModel):
    """Response returned after creating a survey."""

    survey_id: int


class CreateSurveyAnswersResponse(BaseModel):
    """Response returned after submitting survey answers."""

    assessment_id: int


class RankingItem(BaseModel):
    """Single ranking entry for a user."""

    user: str
    rank: int
    avg_score: float


class SurveyMetricsResponse(BaseModel):
    """Survey ranking results and summary."""

    ranking: list[RankingItem]
    summary: str

class SurveyBasicResponse(BaseModel):
    """Basic survey definition."""
    id: int
    topic: str