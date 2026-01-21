from langchain_openai import ChatOpenAI

from core.config import settings
from schema.llm.questions import QuestionsStructuredOutput
from shared.prompt import SURVEY_GENERATOR


def survey_generator_agent(topic: str) -> QuestionsStructuredOutput:
    """
    Generate a survey question (open or multiple-choice) for a given topic.

    Args:
        topic: Topic used to generate the question.

    Returns:
        A structured survey question.
    """
    llm = ChatOpenAI(
        model=settings.GEN_AI_MODEL,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(QuestionsStructuredOutput)

    chain = SURVEY_GENERATOR | structured_llm

    return chain.invoke({"topic": topic})
