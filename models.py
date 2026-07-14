from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ------------------------
# User Model
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # One interviewer can have many interviews
    interviews = relationship("Interview", back_populates="interviewer")


# ------------------------
# Candidate Model
# ------------------------
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    experience = Column(Float, nullable=False)
    skill_set = Column(String, nullable=False)
    application_status = Column(
        String,
        default="Applied"
    )

    # One candidate can attend multiple interviews
    interviews = relationship(
        "Interview",
        back_populates="candidate",
        cascade="all, delete"
    )


# ------------------------
# Interview Model
# ------------------------
class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    interviewer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    interview_date = Column(Date, nullable=False)
    interview_time = Column(Time, nullable=False)

    interview_mode = Column(String, nullable=False)
    status = Column(
        String,
        default="Scheduled"
    )

    # Relationships
    candidate = relationship(
        "Candidate",
        back_populates="interviews"
    )

    interviewer = relationship(
        "User",
        back_populates="interviews"
    )

    feedback = relationship(
        "Feedback",
        back_populates="interview",
        uselist=False,
        cascade="all, delete"
    )


# ------------------------
# Feedback Model
# ------------------------
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        unique=True,
        nullable=False
    )

    technical_rating = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    remarks = Column(String, nullable=True)

    interview = relationship(
        "Interview",
        back_populates="feedback"
    )