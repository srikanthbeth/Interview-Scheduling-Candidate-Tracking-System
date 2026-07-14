from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth
from database import get_db
import models


# ------------------------
# Database Dependency
# ------------------------
def get_database():
    db: Session = next(get_db())
    try:
        yield db
    finally:
        db.close()


# ------------------------
# Get Current Logged-in User
# ------------------------
def get_current_user(
    current_user: models.User = Depends(auth.get_current_user),
):
    return current_user


# ------------------------
# Admin Only
# ------------------------
def admin_required(
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can perform this action"
        )
    return current_user


# ------------------------
# HR Only
# ------------------------
def hr_required(
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != "HR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can perform this action"
        )
    return current_user


# ------------------------
# Interviewer Only
# ------------------------
def interviewer_required(
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != "Interviewer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Interviewer can perform this action"
        )
    return current_user


# ------------------------
# Admin or HR
# ------------------------
def admin_or_hr_required(
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    return current_user


# ------------------------
# Admin, HR, or Interviewer
# ------------------------
def authenticated_user(
    current_user: models.User = Depends(auth.get_current_user),
):
    return current_user