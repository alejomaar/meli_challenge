from typing import Optional

from pydantic import BaseModel


class SurveyAnswers(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None
    text_answer: Optional[str] = None

class SurveyAnswersPayload(BaseModel):
    answers: list[SurveyAnswers]
