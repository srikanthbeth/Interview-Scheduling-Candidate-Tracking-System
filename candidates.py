from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


# ------------------------
# Create Candidate
# ------------------------
@router.post("/", response_model=schemas.CandidateResponse)
def create_candidate(
    candidate: schemas.CandidateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    existing_candidate = crud.get_candidate_by_email(db, candidate.email)

    if existing_candidate:
        raise HTTPException(
            status_code=400,
            detail="Candidate email already exists"
        )

    return crud.create_candidate(db, candidate)


# ------------------------
# Get All Candidates
# ------------------------
@router.get("/", response_model=List[schemas.CandidateResponse])
def get_candidates(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    skip = (page - 1) * limit

    return crud.get_candidates(db, skip, limit)


# ------------------------
# Get Candidate By ID
# ------------------------
@router.get("/{candidate_id}", response_model=schemas.CandidateResponse)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    candidate = crud.get_candidate(db, candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


# ------------------------
# Update Candidate
# ------------------------
@router.put("/{candidate_id}", response_model=schemas.CandidateResponse)
def update_candidate(
    candidate_id: int,
    candidate: schemas.CandidateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    updated_candidate = crud.update_candidate(
        db,
        candidate_id,
        candidate
    )

    if not updated_candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return updated_candidate

# ------------------------
# Update Candidate Status
# ------------------------
@router.put(
    "/{candidate_id}/status",
    response_model=schemas.CandidateResponse
)
def update_candidate_status(
    candidate_id: int,
    status_update: schemas.CandidateStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    # Only HR can update final status
    if current_user.role != "HR":
        raise HTTPException(
            status_code=403,
            detail="Only HR can update candidate status"
        )

    candidate = crud.update_candidate_status(
        db,
        candidate_id,
        status_update.application_status
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


# ------------------------
# Delete Candidate
# ------------------------
@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete candidates"
        )

    deleted_candidate = crud.delete_candidate(
        db,
        candidate_id
    )

    if not deleted_candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "message": "Candidate deleted successfully"
    }