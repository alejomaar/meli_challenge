from fastapi import HTTPException, status
from model import (
    Answer,
    Assessment,
    FeedbackAnswer,
    Option,
    Question,
    QuestionType,
    Survey,
    User,
)
from schema.api import (
    CreateSurveyAnswersResponse,
    CreateSurveyPayload,
    CreateSurveyResponse,
    SurveyMetricsResponse,
)
from schema.api.survey import SurveyAnswersPayload
from schema.llm.questions import ClosedQuestion, QuestionsStructuredOutput
from service.agents import use_case_create_survey_generator
from shared.prompt import SUMMARY_TEMPLATE
from sqlalchemy import case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def use_case_get_survey(
    survey_id: int,
    db: AsyncSession ,
):
    """
    Retrieve basic survey information.
    """

    survey = await db.scalar(
        select(Survey.id, Survey.topic).where(Survey.id == survey_id)
    )

    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )

    return survey


async def use_case_create_survey(
    payload: CreateSurveyPayload, db: AsyncSession
):
    """
    Create a new survey.

    A survey is generated automatically based on a predefined topic.
    The survey includes open and closed questions and is stored
    together with all its questions and options.

    Returns:
        The identifier of the newly created survey.
    """

    # Invoke
    result: QuestionsStructuredOutput = use_case_create_survey_generator(payload.topic)
    survey = Survey(topic=payload.topic)

    for q in result.open_questions:
        question = Question(
            description=q.description,
            question_type=QuestionType.OPEN,
            hint=None,
        )
        survey.questions.append(question)

    for q in result.closed_questions:
        question = Question(
            description=q.description,
            question_type=QuestionType.CLOSED,
            hint=q.hint ,
        )
        survey.questions.append(question)

        for o in q.options:
            option = Option(
                text=o.text,
                is_correct=o.is_correct,
            )
            question.options.append(option)

    db.add(survey)

    await db.flush() 
    await db.commit()

    return CreateSurveyResponse(survey_id=survey.id)



async def use_case_create_survey_answers(
    survey_id: int,
    payload: SurveyAnswersPayload,
    db: AsyncSession ,
    user: User,
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

    user_id = user.id
    try:
        # 1. Ensure survey exists
        exists = await db.scalar(select(Survey.id).where(Survey.id == survey_id))
        if not exists:
            raise HTTPException(status_code=404, detail="Survey not found")

        # 2. Create assessment (may violate uq_user_survey)
        assessment = Assessment(user_id=user_id, survey_id=survey_id)
        db.add(assessment)
        await db.flush()  # constraint is checked here

        # 3. Load survey questions
        result = await db.execute(
            select(Question.id, Question.question_type).where(
                Question.survey_id == survey_id
            )
        )
        question_map = {q.id: q.question_type for q in result}

        survey_question_ids = set(question_map.keys())
        payload_question_ids = {a.question_id for a in payload.answers}

        if payload_question_ids != survey_question_ids:
            raise HTTPException(
                status_code=400,
                detail="All survey questions must be answered",
            )

        # 4. Build answers
        answers_db: list[Answer] = []

        for a in payload.answers:
            q_type = question_map[a.question_id]

            if q_type == QuestionType.CLOSED and not a.selected_option_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {a.question_id} requires selected_option_id",
                )

            if q_type == QuestionType.OPEN and not a.text_answer:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {a.question_id} requires text_answer",
                )

            answers_db.append(
                Answer(
                    assessment_id=assessment.id,
                    question_id=a.question_id,
                    selected_option_id=a.selected_option_id,
                    text_answer=a.text_answer,
                )
            )

        db.add_all(answers_db)
        await db.commit()

    except IntegrityError as exc:

        # PostgreSQL-safe check (constraint name)
        if "uq_user_survey" in str(exc.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already answered this survey",
            )

        raise  # unknown integrity error → rethrow

    return CreateSurveyAnswersResponse(assessment_id=assessment.id)


async def use_case_get_survey_metrics(
    survey_id: int,
    ranking_size: int,
    db: AsyncSession,
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

    # ---------- RANKING (Top K) ----------

    avg_score = func.avg(FeedbackAnswer.score)

    ranking_stmt = (
        select(
            User.nickname.label("user"),
            avg_score.label("avg_score"),
            func.dense_rank().over(order_by=avg_score.desc()).label("rank"),
        )
        .join(Assessment, Assessment.user_id == User.id)
        .join(FeedbackAnswer, FeedbackAnswer.assessment_id == Assessment.id)
        .where(Assessment.survey_id == survey_id)
        .group_by(User.nickname)
        .order_by(avg_score.desc())
        .limit(ranking_size)
    )

    ranking_result = await db.execute(ranking_stmt)
    ranking_rows = ranking_result.all()

    if not ranking_rows:
        raise HTTPException(
            status_code=404,
            detail="No feedback metrics found for this survey",
        )

    ranking = [
        {
            "user": row.user,
            "rank": row.rank,
            "avg_score": round(float(row.avg_score), 3),
        }
        for row in ranking_rows
    ]

    # ---------- SURVEY STATS FOR SUMMARY ----------

    stats_stmt = (
        select(
            Survey.topic,
            func.count(Question.id).label("total_questions"),
            func.sum(
                case(
                    (Question.question_type == QuestionType.OPEN, 1),
                    else_=0,
                )
            ).label("open_questions"),
            func.sum(
                case(
                    (Question.question_type == QuestionType.CLOSED, 1),
                    else_=0,
                )
            ).label("closed_questions"),
        )
        .join(Question, Question.survey_id == Survey.id)
        .where(Survey.id == survey_id)
        .group_by(Survey.topic)
    )

    stats = (await db.execute(stats_stmt)).one()

    best_user = ranking[0]["user"]

    # ---------- SUMMARY ----------
    summary = SUMMARY_TEMPLATE.format(
        topic=stats.topic,
        total_questions=stats.total_questions,
        open_questions=stats.open_questions,
        closed_questions=stats.closed_questions,
        best_user=best_user,
    )

    return SurveyMetricsResponse(
        ranking=ranking,
        summary=summary,
    )
