from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from core.model import Base


class QuestionType(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"


class Survey(Base):
    __tablename__ = "survey"

    id = Column(Integer, primary_key=True)
    topic = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    questions = relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan",
    )

    assessments = relationship(
        "Assessment",
        back_populates="survey",
    )


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("survey.id"), nullable=False)

    description = Column(Text, nullable=False)
    question_type = Column(
        SAEnum(QuestionType, name="question_type_enum"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    survey = relationship(
        "Survey",
        back_populates="questions",
    )

    options = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    answers = relationship(
        "Answer",
        back_populates="question",
    )


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    question = relationship(
        "Question",
        back_populates="options",
    )


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    assessments = relationship(
        "Assessment",
        back_populates="user",
    )


class Assessment(Base):
    __tablename__ = "assessment"
    __table_args__ = (
        UniqueConstraint("user_id", "survey_id", name="uq_user_survey"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("survey.id"), nullable=False)

    started_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    finished_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="assessments",
    )

    survey = relationship(
        "Survey",
        back_populates="assessments",
    )

    answers = relationship(
        "Answer",
        back_populates="assessment",
        cascade="all, delete-orphan",
    )

    feedback = relationship(
        "Feedback",
        back_populates="assessment",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Answer(Base):
    __tablename__ = "answer"
    __table_args__ = (
        UniqueConstraint("assessment_id", "question_id", name="uq_answer_per_question"),
    )

    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("option.id"))
    text_answer = Column(Text)

    is_correct = Column(Boolean)
    score = Column(Float)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    assessment = relationship(
        "Assessment",
        back_populates="answers",
    )

    question = relationship(
        "Question",
        back_populates="answers",
    )

    option = relationship("Option")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False, unique=True)

    summary_text = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    assessment = relationship(
        "Assessment",
        back_populates="feedback",
    )
