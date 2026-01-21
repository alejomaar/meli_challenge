# 🧠 Interactive Trivia / Quiz Agent

## Overview

This project implements an **interactive trivia / quiz system powered by LLM agents**.

Users answer quizzes on a given topic, receive **educational feedback**, and are later **ranked** based on their performance.
The system focuses on **learning and feedback**, not just scoring.

Developed as part of **Ejercicio 2: Agente de Trivia / Quiz Interactivo**.

---

## 🎯 What the system does

* Generate trivia quizzes automatically from a topic
* Mix **open** and **multiple-choice** questions
* Evaluate answers objectively
* Provide constructive, encouraging feedback
* Rank participants and generate a summary report

---

## 🧠 Conceptual flow

```
Survey
 └── Questions (open / closed)
      └── Options (closed only)

User
 └── Assessment
      └── Answers
           └── FeedbackAnswer

Survey
 └── Metrics (ranking + summary)
```

---

## 🔐 Authentication (Mocked)

Authentication is intentionally simple:

```
X-User-Id: <user_id>
```

No passwords, no tokens.

---

## 📊 API Examples (with images)

---

## 👤 User

**Entity**: User
Represents a participant in the trivia system.

**Endpoint**

```
POST /user
```

**Payload**

```json
{
  "nickname": "pedro"
}
```

**Result**

```md
![User](./img/user.png)
```

---

## 🧠 Survey

**Entity**: Survey
Represents a trivia game for a specific topic.

**Endpoint**

```
POST /survey
```

**Payload**

```json
{
  "topic": "matematicas"
}
```

**Result**

```md
![Survey](./img/survey.png)
```

---

## ❓ Question

**Entity**: Question
Represents a single trivia question (open or closed).

Questions are generated automatically when a survey is created.

**Result**

```md
![Question](./img/question.png)
```

---

## 🔘 Option

**Entity**: Option
Represents a possible answer for a closed question.

Options are generated automatically together with closed questions.

**Result**

```md
![Option](./img/option.png)
```

---

## 📝 Assessment

**Entity**: Assessment
Represents **one user answering one survey**.

**Endpoint**

```
POST /survey/{survey_id}/answers
```

**Headers**

```
X-User-Id: 3
```

**Payload**

```json
{
  "answers": [
    {
      "question_id": 65,
      "text_answer": "Un número primo no se puede expresar como multiplicación de otros"
    }
  ]
}
```

**Result**

```md
![Assessment](./img/assesment.png)
```

---

## ✍️ Answer

**Entity**: Answer
Represents a single response to a question.

**Payload fragment**

```json
{
  "question_id": 66,
  "selected_option_id": 168
}
```

**Result**

```md
![Answer](./img/answer.png)
```

---

## 💬 FeedbackAnswer

**Entity**: FeedbackAnswer
Stores educational feedback and an internal score for each answer.

**Endpoint**

```
POST /assesment/{assessment_id}/feedback
```

**Result**

```md
![FeedbackAnswer](./img/feedback_answer.png)
```

---

## 🏆 Survey Metrics (Ranking)

**Entity**: Aggregated Results
Represents ranking and summary for a survey.

**Endpoint**

```
GET /survey/{survey_id}/metrics?ranking_size=3
```

**Result**

![Survey Metrics](./img/survey.png)

---

## 🧠 Why this design works

* Feedback is **educational**, not punitive
* Scores are internal and never shown directly
* LLM usage is controlled and explainable
* Strong typing and constraints everywhere
* Easy to extend with real authentication and analytics

---

## 🛠 Tech Stack

**Backend**

* FastAPI
* Pydantic v2
* SQLAlchemy 2.0
* Alembic
* PostgreSQL

**LLM**

* LangChain
* OpenAI

---

## 🚀 Run the project

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make run
```

