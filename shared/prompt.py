from langchain_core.prompts import ChatPromptTemplate

OPEN_QUESTION_EVALUATOR = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un evaluador. Dada una pregunta y la respuesta de un usuario, "
            "califica qué tan buena es la respuesta en una escala de 0 a 1. "
            "Sé alentador y enfócate en los puntos fuertes.",
        ),
        ("human", "{question_and_answer}"),
    ]
)


SURVEY_GENERATOR = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un generador de cuestionarios amigable. Dado un tema, genera "
            "varias preguntas de conocimiento, tanto abiertas como de opción múltiple. "
            "Las preguntas no deben basarse en preferencias personales y deben poder "
            "entenderse y evaluarse de forma objetiva. "
            "No repitas preguntas. Mantén un tono claro, atractivo y amigable.",
        ),
        ("human", "{topic}"),
    ]
)


SUMMARY_TEMPLATE = (
    "Se obtuvo un ranking para la encuesta '{topic}', con un total de "
    "{total_questions} preguntas ({open_questions} abiertas y "
    "{closed_questions} cerradas). "
    "El mejor desempeño general fue de {best_user}."
)


OK_ANSWER = "¡Respuesta correcta! Buen trabajo 🎉"
