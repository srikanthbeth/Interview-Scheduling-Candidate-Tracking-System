from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, time
import re


# ==========================
# User Schemas
# ==========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================
# Candidate Schemas
# ==========================

class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    experience: float = Field(..., ge=0)
    skill_set: str
    application_status: str = "Applied"

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")
        return value


class CandidateResponse(CandidateCreate):
    id: int

    class Config:
        from_attributes = True

        # ==========================
# Candidate Status Update
# ==========================

class CandidateStatusUpdate(BaseModel):
    application_status: str


# ==========================
# Interview Schemas
# ==========================

class InterviewCreate(BaseModel):
    candidate_id: int
    interviewer_id: int
    interview_date: date
    interview_time: time
    interview_mode: str
    status: str = "Scheduled"


class InterviewResponse(InterviewCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================
# Feedback Schemas
# ==========================

class FeedbackCreate(BaseModel):
    interview_id: int
    technical_rating: int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    remarks: str


class FeedbackResponse(FeedbackCreate):
    id: int

    class Config:
        from_attributes = True