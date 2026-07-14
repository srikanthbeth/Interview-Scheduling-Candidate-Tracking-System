from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


# ------------------------
# Create Interview
# ------------------------
@router.post("/", response_model=schemas.InterviewResponse)
def create_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    result = crud.create_interview(db, interview)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate or Interviewer not found"
        )

    if result == "duplicate":
        raise HTTPException(
            status_code=400,
            detail="Interview already scheduled for this interviewer at the selected date and time."
        )

    return result


# ------------------------
# Get All Interviews
# ------------------------
@router.get("/", response_model=List[schemas.InterviewResponse])
def get_interviews(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    skip = (page - 1) * limit

    interviews = crud.get_interviews(db, skip, limit)

    # Interviewer can view only assigned interviews
    if current_user.role == "Interviewer":
        interviews = [
            interview
            for interview in interviews
            if interview.interviewer_id == current_user.id
        ]

    return interviews


# ------------------------
# Get Interview By ID
# ------------------------
@router.get("/{interview_id}", response_model=schemas.InterviewResponse)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    interview = crud.get_interview(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    if (
        current_user.role == "Interviewer"
        and interview.interviewer_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only view your assigned interviews."
        )

    return interview


# ------------------------
# Update Interview
# ------------------------
@router.put("/{interview_id}", response_model=schemas.InterviewResponse)
def update_interview(
    interview_id: int,
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    updated = crud.update_interview(
        db,
        interview_id,
        interview
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    return updated