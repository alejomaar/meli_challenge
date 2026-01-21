from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from core.model import Base


def utcnow():
    return datetime.now(timezone.utc)


class QuestionType(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"


class Survey(Base):
    __tablename__ = "survey"

    topic = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

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

    survey_id = Column(Integer, ForeignKey("survey.id"), nullable=False)

    description = Column(Text, nullable=False)
    hint = Column(Text)
    question_type = Column(
        SAEnum(QuestionType, name="question_type_enum"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

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

    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    question = relationship(
        "Question",
        back_populates="options",
    )


class User(Base):
    __tablename__ = "user"

    nickname = Column(String(100), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    assessments = relationship(
        "Assessment",
        back_populates="user",
    )


class Assessment(Base):
    __tablename__ = "assessment"
    __table_args__ = (
        UniqueConstraint("user_id", "survey_id", name="uq_user_survey"),
    )

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("survey.id"), nullable=False)

    started_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    finished_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

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

    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("option.id"))
    text_answer = Column(Text)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

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

    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False, unique=True)

    summary_text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    assessment = relationship(
        "Assessment",
        back_populates="feedback",
    )


class FeedbackAnswer(Base):
    __tablename__ = "feedback_answer"
    __table_args__ = (
        UniqueConstraint("assessment_id", "answer_id", name="uq_feedback_answer"),
    )

    assessment_id = Column(
        Integer,
        ForeignKey("assessment.id"),
        nullable=False,
    )
    answer_id = Column(
        Integer,
        ForeignKey("answer.id"),
        nullable=False,
    )

    feedback = Column(Text, nullable=False)
    score = Column(
        Float,
        nullable=False,
        doc="Score for the answer, between 0 and 1",
    )

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    assessment = relationship(
        "Assessment",
        backref="feedback_answers",
    )

    answer = relationship(
        "Answer",
        backref="feedback",
        uselist=False,
    )
