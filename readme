# 🧠 Interactive Trivia / Quiz Agent

## Overview

This project implements an **interactive trivia (quiz) system powered by LLM agents**.
Users participate in quizzes on a given topic, answer open and closed questions, receive **educational feedback**, and are later **ranked** based on their performance.

The system is designed as a **multi-agent backend service**, capable of handling multiple participants, evaluating answers objectively, and generating meaningful summaries and rankings.

This project was developed as part of **Ejercicio 2: Agente de Trivia/Quiz Interactivo**.

---

## 🎯 Functional Goals

The system supports the following capabilities:

1. **Question generation**

   * Automatically generates open and closed trivia questions based on a topic.
   * Questions are knowledge-based (not opinions) and objectively evaluable.

2. **Answer evaluation**

   * Closed questions are evaluated via correctness.
   * Open questions are evaluated using an LLM-based evaluator.

3. **Data persistence**

   * Surveys, questions, answers, assessments, and feedback are stored in PostgreSQL.

4. **Educational feedback**

   * Each answer receives constructive, encouraging feedback.
   * The internal numeric score is **never shown to participants**.

5. **Result analysis**

   * Participant performance is aggregated.
   * Rankings are generated based on average scores.

6. **Reporting**

   * A final summary report is produced describing:

     * Survey structure
     * Number of questions
     * Best overall participant

---

## 🧩 Architecture

The system follows a **layered architecture**:

```
API (FastAPI)
 ├── Routers (survey, assessment, user)
 ├── Dependencies (auth, db)
 ├── Schemas (Pydantic)
 ├── Services (LLM agents)
 ├── Persistence (SQLAlchemy models)
 └── Database (PostgreSQL + Alembic)
```

### Key Components

| Layer        | Description                                           |
| ------------ | ----------------------------------------------------- |
| **Routers**  | FastAPI endpoints (`/survey`, `/assessment`, `/user`) |
| **Schemas**  | Pydantic models for request/response validation       |
| **Agents**   | LLM-based agents using LangChain                      |
| **Models**   | SQLAlchemy ORM entities                               |
| **Database** | PostgreSQL with Alembic migrations                    |
| **Prompts**  | Centralized prompt templates                          |

---

## 🤖 LLM Agents

The project uses **LangChain + OpenAI** for intelligent behavior.

### Agents implemented

* **Survey Generator Agent**

  * Generates multiple open and closed trivia questions for a topic.
* **Open Question Evaluator Agent**

  * Scores and provides encouraging feedback for open answers.

Prompts are defined in `shared/prompt.py` and written in **Spanish**.

---

## 📁 Project Structure

```
.
├── alembic/                # Database migrations
├── api.py                  # FastAPI app entrypoint
├── core/                   # Config, DB session, dependencies
├── model/                  # SQLAlchemy ORM models
├── router/                 # API routes (survey, assessment, user)
├── schema/                 # Pydantic schemas
│   ├── api/                # API request/response models
│   └── llm/                # LLM structured outputs
├── service/
│   └── agents/             # LangChain agents
├── shared/
│   └── prompt.py           # Centralized prompt templates
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

---

## 🧪 Technical Stack

### Backend

* **FastAPI** `0.115.4`
* **Pydantic v2**
* **SQLAlchemy 2.0**
* **Alembic**
* **PostgreSQL**
* **asyncpg / pg8000**

### LLM

* **LangChain**
* **langchain-openai**

---

## 🔐 Authentication (Mocked)

Authentication is intentionally simple:

* Requests include header:

  ```
  X-User-Id: <user_id>
  ```
* No passwords or tokens.
* Easy to replace with real authentication later.

---

## 🚀 Installation

### 1️⃣ Create virtual environment

```bash
python3.10 -m venv .venv
```

### 2️⃣ Activate environment

```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the application

```bash
make run
```

This will start the FastAPI server using the configuration defined in the `Makefile`.

---

## 🗄️ Database Migrations

Alembic is used for schema management.

Example migrations include:

* Initial tables
* DateTime updates
* Feedback answer table
* Hint support for closed questions

---

## 📊 API Highlights

| Endpoint                         | Description           |
| -------------------------------- | --------------------- |
| `POST /user`                     | Create a new user     |
| `POST /survey`                   | Generate a new survey |
| `POST /survey/{id}/answers`      | Submit survey answers |
| `POST /assessment/{id}/feedback` | Generate feedback     |
| `GET /survey/{id}/metrics`       | Ranking & summary     |

---
## 🧠 Database Design

his is the data model for an **interactive trivia / quiz system**.

* A **Survey** defines a quiz topic
* A **User** participates in a survey
* Each participation creates an **Assessment**
* Users answer **Questions**
* Answers receive **Feedback**
* Results can be analyzed and ranked

---

## Main entities and relationships

### 🧠 Survey

* Represents a quiz (e.g. *Elementary maths*)
* Contains multiple **Questions**
* Is answered by many users (via assessments)

---

### ❓ Question

* Belongs to a **Survey**
* Can be **OPEN** or **CLOSED**
* Has:

  * `description` (the question text)
  * `hint` (used when a closed question is answered incorrectly)
* Closed questions have multiple **Options**

---

### 🔘 Option

* Belongs to a **Question**
* Represents a multiple-choice option
* Exactly **one option is correct**

---

### 👤 User

* Represents a participant
* Identified by a nickname
* Can take many surveys

---

### 📝 Assessment

* Represents **one user answering one survey**
* Links **User ↔ Survey**
* Tracks when the quiz started and finished
* Has many **Answers**
* Has one overall **Feedback** summary

> This is the core unit of participation.

---

### ✍️ Answer

* Represents a user’s answer to a single question
* Belongs to:

  * one **Assessment**
  * one **Question**
* Stores:

  * selected option (for closed questions)
  * text answer (for open questions)

---

### 💬 FeedbackAnswer

* Feedback **per answer**
* Belongs to:

  * one **Assessment**
  * one **Answer**
* Stores:

  * educational feedback text
  * internal score (0–1)

## 🧠 Design Decisions

* **Scores are internal only**
  Users never see numeric scores during the quiz.

* **Feedback is constructive**
  Always educational, positive, and encouraging.

* **LLM used only where needed**
  Closed questions use rules, open questions use LLMs.

* **Strong typing everywhere**
  Type hints and Pydantic models across the codebase.

* **Future-proof architecture**
  Easy to extend with:

  * Real auth
  * Difficulty levels


# Example 

## User

**Entity**: User
Represents a participant in the trivia system.

**Endpoint**

```
POST /user
```

**Params (payload)**

```json
{
  "nickname": "pedro"
}
```

**Image**
[image][img/user.png]

---

## Survey

**Entity**: Survey
Represents a trivia game for a specific topic.

**Endpoint**

```
POST /survey
```

**Params (payload)**

```json
{
  "topic": "matematicas"
}
```

**Image**
[image][img/survey.png]

---

## Question

**Entity**: Question
Represents a single trivia question (open or closed) generated for a survey.

**Endpoint**

```
POST /survey
```

(Questions are generated automatically when a survey is created)

**Params**

* No direct payload (generated by LLM)

**Image**
[image][img/question.png]

---

## Option

**Entity**: Option
Represents a possible answer for a closed question.

**Endpoint**

```
POST /survey
```

(Options are generated automatically with closed questions)

**Params**

* No direct payload

**Image**
[image][img/option.png]

---

## Assessment

**Entity**: Assessment
Represents one user answering one survey.

**Endpoint**

```
POST /survey/{survey_id}/answers
```

**Params (headers + payload)**

```
X-User-Id: 3
```

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

**Image**
[image][img/assesment.png]

---

## Answer

**Entity**: Answer
Represents a single response to a question.

**Endpoint**

```
POST /survey/{survey_id}/answers
```

**Params (payload fragment)**

```json
{
  "question_id": 66,
  "selected_option_id": 168
}
```

**Image**
[image][img/answer.png]

---

## FeedbackAnswer

**Entity**: FeedbackAnswer
Stores feedback and internal score for an answer.

**Endpoint**

```
POST /assesment/{assessment_id}/feedback
```

**Params**

* No payload (feedback is generated from stored answers)

**Image**
[image][img/feedback_answer.png]

---

## Survey Metrics (Ranking)

**Entity**: Aggregated Results
Represents ranking and summary for a survey.

**Endpoint**

```
GET /survey/{survey_id}/metrics?ranking_size=3
```

**Params**

* `ranking_size`: number of top users to return

**Image**
[image][img/survey.png]

