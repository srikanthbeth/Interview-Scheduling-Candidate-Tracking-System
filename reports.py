from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ------------------------
# Search Candidates by Skill Set
# ------------------------
@router.get("/search", response_model=List[schemas.CandidateResponse])
def search_candidates(
    skill: str,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    return crud.search_candidates(db, skill)


# ------------------------
# Filter Interviews
# ------------------------
@router.get("/interviews", response_model=List[schemas.InterviewResponse])
def filter_interviews(
    status: str = None,
    interviewer_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    interviews = crud.filter_interviews(
        db,
        status=status,
        interviewer_id=interviewer_id
    )

    # Interviewers can view only their own interviews
    if current_user.role == "Interviewer":
        interviews = [
            interview
            for interview in interviews
            if interview.interviewer_id == current_user.id
        ]

    return interviews


# ------------------------
# Selected Candidates
# ------------------------
@router.get("/selected", response_model=List[schemas.CandidateResponse])
def selected_candidates(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    return crud.selected_candidates(db)


# ------------------------
# Rejected Candidates
# ------------------------
@router.get("/rejected", response_model=List[schemas.CandidateResponse])
def rejected_candidates(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    return crud.rejected_candidates(db)