from core.deps import get_current_user, get_db
from fastapi import APIRouter, Depends, status
from model import (
    User,
)
from schema.api import (
    CreateSurveyAnswersResponse,
    CreateSurveyPayload,
    CreateSurveyResponse,
    SurveyMetricsResponse,
)
from schema.api.survey import SurveyAnswersPayload, SurveyBasicResponse
from service.survey import (
    use_case_create_survey,
    use_case_create_survey_answers,
    use_case_get_survey,
    use_case_get_survey_metrics,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/survey",
    tags=["survey"]
)


@router.get(
    "/{survey_id}",
    status_code=status.HTTP_200_OK,
    response_model=SurveyBasicResponse,
)
async def get_survey(
    survey_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve basic survey information.
    """

    return await use_case_get_survey(survey_id, db)


@router.post("/", response_model=CreateSurveyResponse)
async def create_survey(
    payload: CreateSurveyPayload, db: AsyncSession = Depends(get_db)
):
    """
    Create a new survey.

    A survey is generated automatically based on a predefined topic.
    The survey includes open and closed questions and is stored
    together with all its questions and options.

    Returns:
        The identifier of the newly created survey.
    """

    return await use_case_create_survey(payload, db)


@router.post(
    "/{survey_id}/answers",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateSurveyAnswersResponse,
)
async def create_survey_answers(
    survey_id: int,
    payload: SurveyAnswersPayload,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Submit answers for a survey.

    This endpoint records a complete set of answers for a given survey
    on behalf of the authenticated user. Each question in the survey
    must be answered exactly once.

    A user can only submit answers to the same survey one time.

    Parameters:
        survey_id: Identifier of the survey being answered.
        payload: Collection of answers provided by the user.

    Returns:
        The identifier of the created assessment.
    """

    return await use_case_create_survey_answers(survey_id, payload, db, user)


@router.get(
    "/{survey_id}/metrics",
    status_code=status.HTTP_200_OK,
    response_model=SurveyMetricsResponse,
)
async def get_survey_metrics(
    survey_id: int,
    ranking_size: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve performance metrics for a survey.

    This endpoint computes a ranking of users based on their
    average feedback score for the survey. It also provides
    a human-readable summary describing the survey structure
    and overall best performance.

    Parameters:
        survey_id: Identifier of the survey.
        ranking_size: Maximum number of top-ranked users to return.

    Returns:
        A ranking of users with their average scores and a summary
        describing the survey results.
    """


    return await use_case_get_survey_metrics(survey_id, ranking_size, db)
