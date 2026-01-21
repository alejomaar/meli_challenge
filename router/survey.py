from fastapi import APIRouter, FastAPI, HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from schema.llm.quiz import Option, QuizItem

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
async def create_survey():
    """Create a new survey - Not Yet Implemented"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Wrap LLM with structured output
    structured_llm = llm.with_structured_output(QuizItem)

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a quiz generator. Return a multiple-choice question."),
        ("human", "{topic}")
    ])

    # Chain
    chain = prompt | structured_llm

    # Invoke
    result = chain.invoke({
        "topic": "Create a multiple choice question about Python decorators"
    })
    print(result)
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="POST method for /survey is not implemented yet."
    )

@router.delete("/{survey_id}")
async def delete_survey(survey_id: int):
    """Delete a survey - Not Yet Implemented"""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"DELETE method for survey {survey_id} is not implemented yet."
    )

