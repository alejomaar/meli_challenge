from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from crud import CrudSurvey
from model import Option, Question, QuestionType, Survey
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
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a quiz generator. Return a multiple-choice question and open questions"),
        ("human", "{topic}")
    ])

    # Chain
    chain = prompt | structured_llm
    topic = "Climate change"
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


@router.delete("/{survey_id}")
async def delete_survey(survey_id: int):
    """Delete a survey - Not Yet Implemented"""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"DELETE method for survey {survey_id} is not implemented yet."
    )
