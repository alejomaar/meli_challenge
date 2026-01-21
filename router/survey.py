from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.deps import get_db
from crud import CrudSurvey
from model import Answer, Assessment, Option, Question, QuestionType, Survey
from schema.api.survey import SurveyAnswersPayload
from schema.llm.feedback_open_question import FeedbackOpenQuestion
from schema.llm.questions import ClosedQuestion, OpenQuestion
from schema.llm.questions import Option as llmOption
from schema.llm.questions import QuestionsStructuredOutput

router = APIRouter(
    prefix="/survey",
    tags=["survey"]
)

@router.get("/")
async def get_survey():
    """Retrieve survey data - Not Yet Implemented"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="GET method for /survey is not implemented yet."
    )


@router.post("/")
async def create_survey(db: AsyncSession = Depends(get_db)):
    """Create a new survey - Not Yet Implemented"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    crud_survey = CrudSurvey(db)
    structured_llm = llm.with_structured_output(QuestionsStructuredOutput)

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a friendly quiz generator. Given a topic, create either an open question "
                "or a multiple-choice question. Never repeat questions. Keep the tone clear, "
                "engaging, and friendly.",
            ),
            ("human", "{topic}"),
        ]
    )

    # Chain
    chain = prompt | structured_llm
    topic = "Elementary maths"
    # Invoke
    result: QuestionsStructuredOutput = chain.invoke({"topic": topic})
    survey = Survey(topic=topic)

    for q in result.questions:
        question = Question(
            description=q.description,
            question_type=(
                QuestionType.CLOSED
                if isinstance(q, ClosedQuestion)
                else QuestionType.OPEN
            ),
            hint=q.hint if isinstance(q, ClosedQuestion) else None,
        )
        survey.questions.append(question)

        if isinstance(q, ClosedQuestion):
            for o in q.options:
                option = Option(
                    text=o.text,
                    is_correct=o.is_correct,
                )
                question.options.append(option)

    db.add(survey)

    await db.flush() 
    await db.commit()

    return {"status": "ok"}


@router.post("/{survey_id}/answers", status_code=status.HTTP_201_CREATED)
async def create_survey_answers(
    survey_id: int,
    payload: SurveyAnswersPayload,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    """
    Submit all answers for a survey.

    Creates an assessment for the user and stores one answer per survey question.
    Rejects the request if the survey was already answered by the user.
    """

    user_id = 2  # TODO: replace with authenticated user

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

    return {
        "assessment_id": assessment.id,
    }


@router.post("/{assessment_id}/feedback", status_code=status.HTTP_201_CREATED)
async def create_survey_feedback(
    assessment_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """
    Generate feedback for all answers in an assessment.
    Open questions are evaluated by the LLM.
    Closed questions use correctness + hint.
    """

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
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an evaluator. Given a question and a user's answer, "
                    "score how good the answer is on a scale from 0 to 1. "
                    "Be encouraging and focus on strengths.",
                ),
                ("human", "{question_and_answer}"),
            ]
        )

        structured_llm = llm.with_structured_output(FeedbackOpenQuestion)

        chain = prompt | structured_llm

        batch_inputs = [
            {
                "question_and_answer": (
                    f"Question: {a.question.description}\n"
                    f"User answer: {a.text_answer}"
                )
            }
            for a in open_answers
        ]

        results = await chain.abatch(batch_inputs)

        for answer, feedback in zip(open_answers, results):
            feedback_results.append(
                {
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
                "answer_id": answer.id,
                "score": 1.0 if is_correct else 0.0,
                "feedback": (
                    "¡Respuesta correcta! Buen trabajo 🎉"
                    if is_correct
                    else answer.question.hint
                ),
            }
        )

    return feedback_results
