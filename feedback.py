from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


# ------------------------
# Add Feedback
# ------------------------
@router.post("/", response_model=schemas.FeedbackResponse)
def add_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    # Only Interviewer can submit feedback
    if current_user.role != "Interviewer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Interviewer can submit feedback"
        )

    interview = crud.get_interview(db, feedback.interview_id)

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    # Interviewer can submit feedback only for assigned interview
    if interview.interviewer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can submit feedback only for your assigned interviews"
        )

    result = crud.create_feedback(db, feedback)

    if result == "not_completed":
        raise HTTPException(
            status_code=400,
            detail="Feedback can be added only after interview is completed"
        )

    if result == "exists":
        raise HTTPException(
            status_code=400,
            detail="Feedback already submitted"
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    return result


# ------------------------
# Get Feedback
# ------------------------
@router.get("/{interview_id}", response_model=schemas.FeedbackResponse)
def get_feedback(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    feedback = crud.get_feedback(db, interview_id)

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found"
        )

    interview = crud.get_interview(db, interview_id)

    if (
        current_user.role == "Interviewer"
        and interview.interviewer_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can view only your feedback"
        )

    return feedback