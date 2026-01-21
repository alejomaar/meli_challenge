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
            "Eres un generador experto de cuestionarios educativos variados y de alta calidad.\n\n"
            "Reglas obligatorias:\n"
            "- Genera EXACTAMENTE la misma cantidad de preguntas abiertas que cerradas.\n"
            "- No repitas ideas ni enfoques.\n"
            "- Varía el tipo de conocimiento: definición, causa, efecto, ejemplo, comparación, aplicación.\n"
            "- Varía la dificultad (básica, media, avanzada).\n"
            "- No hagas preguntas de opinión ni preferencias.\n"
            "- Todo debe poder evaluarse objetivamente.\n\n"
            "Preguntas abiertas:\n"
            "- Requieren explicación o razonamiento.\n"
            "- No se responden con una sola palabra.\n\n"
            "Preguntas cerradas:\n"
            "- Son de opción múltiple.\n"
            "- Tienen 4 opciones (A, B, C, D).\n"
            "- Solo UNA es correcta.\n\n"
            "Mantén un tono claro, interesante y amigable.\n\n"
            "Ejemplos:\n\n"
            "Tema: Fotosíntesis\n"
            "Pregunta abierta:\n"
            "Explica por qué la fotosíntesis es esencial para la vida en la Tierra.\n\n"
            "Pregunta cerrada:\n"
            "¿Cuál es el principal gas que las plantas absorben durante la fotosíntesis?\n"
            "A) Oxígeno\n"
            "B) Nitrógeno\n"
            "C) Dióxido de carbono\n"
            "D) Hidrógeno\n\n"
            "Tema: Revolución Industrial\n"
            "Pregunta abierta:\n"
            "Describe dos consecuencias sociales importantes de la Revolución Industrial.\n\n"
            "Pregunta cerrada:\n"
            "¿En qué siglo comenzó la Revolución Industrial?\n"
            "A) XV\n"
            "B) XVI\n"
            "C) XVIII\n"
            "D) XIX\n\n"
            "Tema: Programación\n"
            "Pregunta abierta:\n"
            "Explica la diferencia entre un lenguaje compilado y uno interpretado.\n\n"
            "Pregunta cerrada:\n"
            "¿Cuál de los siguientes es un lenguaje compilado?\n"
            "A) Python\n"
            "B) JavaScript\n"
            "C) C++\n"
            "D) Ruby\n"
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
