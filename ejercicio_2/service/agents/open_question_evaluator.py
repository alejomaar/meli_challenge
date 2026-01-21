from langchain_openai import ChatOpenAI

from core.config import settings
from schema.llm.feedback_open_question import FeedbackOpenQuestion
from schema.llm.questions import QuestionsStructuredOutput
from shared.prompt import OPEN_QUESTION_EVALUATOR


async def open_question_evaluator_agent(
    questions_and_answers: list[str],
) -> list[FeedbackOpenQuestion]:
    """
    Evaluate multiple open-question answers and return structured feedback.

    Args:
        questions_and_answers: List of texts combining question and user answer.

    Returns:
        List of structured feedback results with score and encouraging explanation.
    """
    llm = ChatOpenAI(
        model=settings.GEN_AI_MODEL,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(FeedbackOpenQuestion)

    chain = OPEN_QUESTION_EVALUATOR | structured_llm

    batch_inputs = [
        {"question_and_answer": qa}
        for qa in questions_and_answers
    ]

    return await chain.abatch(batch_inputs)
