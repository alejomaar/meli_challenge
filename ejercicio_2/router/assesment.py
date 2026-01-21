from core.deps import get_db
from fastapi import APIRouter, Depends, status
from schema.api.assesment import CreateAssessmentFeedbackResponse
from service.assesment import use_case_create_assestment_feedback
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/assesment",
    tags=["assesment"]
)


@router.post(
    "/{assessment_id}/feedback",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateAssessmentFeedbackResponse,
)
async def create_assestment_feedback(
    assessment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate feedback for all answers in an assessment.

    This endpoint evaluates each answer in the assessment and produces feedback
    for the user. Open questions receive an AI-generated evaluation, while
    closed questions are scored based on correctness and include a guided
    explanation when answered incorrectly.

    Returns:
        A list of feedback items, one per answer in the assessment.
    """
    return await use_case_create_assestment_feedback(assessment_id, db)
