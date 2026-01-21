from fastapi import HTTPException
from model import Answer, Assessment, FeedbackAnswer, Question, QuestionType
from schema.api.assesment import CreateAssessmentFeedbackResponse
from service.agents import use_case_run_open_question_evaluator
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def use_case_create_assestment_feedback(
    assessment_id: int,
    db: AsyncSession ,
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
    # 0. Reject if feedback already exists
    already_feedback = await db.scalar(
        select(
            exists().where(FeedbackAnswer.assessment_id == assessment_id)
        )
    )
    if already_feedback:
        raise HTTPException(
            status_code=409,
            detail="Feedback was already given for this assessment",
        )

    result = await db.execute(
        select(Answer)
        .join(Assessment)
        .join(Question)
        .options(
            selectinload(Answer.question),
            selectinload(Answer.option),
        )
        .where(Assessment.id == assessment_id)
    )

    answers = result.scalars().all()

    if not answers:
        raise HTTPException(
            status_code=404, detail="No answers found for this assessment"
        )

    open_answers = [a for a in answers if a.question.question_type == QuestionType.OPEN]
    closed_answers = [
        a for a in answers if a.question.question_type == QuestionType.CLOSED
    ]

    feedback_results: list[dict] = []

    # -------- OPEN QUESTIONS (LLM) --------

    if open_answers:

        batch_inputs = [
            {
                "question_and_answer": (
                    f"Question: {a.question.description}\n"
                    f"User answer: {a.text_answer}"
                )
            }
            for a in open_answers
        ]

        results = await use_case_run_open_question_evaluator(batch_inputs)

        for answer, feedback in zip(open_answers, results):
            feedback_results.append(
                {
                    "assessment_id": assessment_id,
                    "answer_id": answer.id,
                    "score": feedback.score,
                    "feedback": feedback.reason,
                }
            )

    # -------- CLOSED QUESTIONS (RULE-BASED) --------

    for answer in closed_answers:
        is_correct = bool(answer.option and answer.option.is_correct)

        feedback_results.append(
            {
                "assessment_id": assessment_id,
                "answer_id": answer.id,
                "score": 1.0 if is_correct else 0.0,
                "feedback": (
                    "¡Respuesta correcta! Buen trabajo 🎉"
                    if is_correct
                    else answer.question.hint
                ),
            }
        )

    all_feedback_answer = [FeedbackAnswer(**item) for item in feedback_results]
    db.add_all(all_feedback_answer)
    await db.commit()

    return CreateAssessmentFeedbackResponse(results=feedback_results)
