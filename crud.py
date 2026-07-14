from sqlalchemy.orm import Session
import models
import schemas
import utils


# ------------------------
# User CRUD
# ------------------------

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = utils.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not utils.verify_password(password, user.password):
        return None

    return user

# ------------------------
# Get Candidate By Email
# ------------------------
def get_candidate_by_email(db: Session, email: str):
    return db.query(models.Candidate).filter(
        models.Candidate.email == email
    ).first()



# ------------------------
# Candidate CRUD
# ------------------------

def create_candidate(db: Session, candidate: schemas.CandidateCreate):

    new_candidate = models.Candidate(
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        experience=candidate.experience,
        skill_set=candidate.skill_set,
        application_status=candidate.application_status
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


def get_candidates(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Candidate).offset(skip).limit(limit).all()


def get_candidate(db: Session, candidate_id: int):

    return db.query(models.Candidate).filter(
        models.Candidate.id == candidate_id
    ).first()


def update_candidate(db: Session, candidate_id: int, candidate: schemas.CandidateCreate):

    db_candidate = get_candidate(db, candidate_id)

    if not db_candidate:
        return None

    db_candidate.name = candidate.name
    db_candidate.email = candidate.email
    db_candidate.phone = candidate.phone
    db_candidate.experience = candidate.experience
    db_candidate.skill_set = candidate.skill_set
    db_candidate.application_status = candidate.application_status

    db.commit()
    db.refresh(db_candidate)

    return db_candidate

# ------------------------
# Update Candidate Status
# ------------------------

def update_candidate_status(
    db: Session,
    candidate_id: int,
    application_status: str
):

    candidate = get_candidate(db, candidate_id)

    if not candidate:
        return None

    candidate.application_status = application_status

    db.commit()
    db.refresh(candidate)

    return candidate


def delete_candidate(db: Session, candidate_id: int):

    db_candidate = get_candidate(db, candidate_id)

    if not db_candidate:
        return None

    db.delete(db_candidate)
    db.commit()

    return db_candidate

# ------------------------
# Interview CRUD
# ------------------------

def create_interview(db: Session, interview: schemas.InterviewCreate):

    # Check whether the candidate exists
    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == interview.candidate_id
    ).first()

    if not candidate:
        return None

    # Check whether the interviewer exists
    interviewer = db.query(models.User).filter(
        models.User.id == interview.interviewer_id
    ).first()

    if not interviewer:
        return None

    # Prevent duplicate interview schedule
    duplicate = db.query(models.Interview).filter(
        models.Interview.interviewer_id == interview.interviewer_id,
        models.Interview.interview_date == interview.interview_date,
        models.Interview.interview_time == interview.interview_time
    ).first()

    if duplicate:
        return "duplicate"

    new_interview = models.Interview(
        candidate_id=interview.candidate_id,
        interviewer_id=interview.interviewer_id,
        interview_date=interview.interview_date,
        interview_time=interview.interview_time,
        interview_mode=interview.interview_mode,
        status=interview.status
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview


def get_interviews(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.Interview).offset(skip).limit(limit).all()


def get_interview(db: Session, interview_id: int):

    return db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()


def update_interview(db: Session, interview_id: int, interview: schemas.InterviewCreate):

    db_interview = get_interview(db, interview_id)

    if not db_interview:
        return None

    db_interview.candidate_id = interview.candidate_id
    db_interview.interviewer_id = interview.interviewer_id
    db_interview.interview_date = interview.interview_date
    db_interview.interview_time = interview.interview_time
    db_interview.interview_mode = interview.interview_mode
    db_interview.status = interview.status

    db.commit()
    db.refresh(db_interview)

    return db_interview

# ------------------------
# Feedback CRUD
# ------------------------

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):

    # Check interview exists
    interview = db.query(models.Interview).filter(
        models.Interview.id == feedback.interview_id
    ).first()

    if not interview:
        return None

    # Business Rule:
    # Feedback only after interview is completed
    if interview.status != "Completed":
        return "not_completed"

    # Prevent duplicate feedback
    existing_feedback = db.query(models.Feedback).filter(
        models.Feedback.interview_id == feedback.interview_id
    ).first()

    if existing_feedback:
        return "exists"

    new_feedback = models.Feedback(
        interview_id=feedback.interview_id,
        technical_rating=feedback.technical_rating,
        communication_rating=feedback.communication_rating,
        remarks=feedback.remarks
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback


def get_feedback(db: Session, interview_id: int):

    return db.query(models.Feedback).filter(
        models.Feedback.interview_id == interview_id
    ).first()


# ------------------------
# Reports & Search
# ------------------------

def search_candidates(db: Session, skill: str):

    return db.query(models.Candidate).filter(
        models.Candidate.skill_set.ilike(f"%{skill}%")
    ).all()


def filter_interviews(
    db: Session,
    status: str = None,
    interviewer_id: int = None
):

    query = db.query(models.Interview)

    if status:
        query = query.filter(
            models.Interview.status == status
        )

    if interviewer_id:
        query = query.filter(
            models.Interview.interviewer_id == interviewer_id
        )

    return query.all()


def selected_candidates(db: Session):

    return db.query(models.Candidate).filter(
        models.Candidate.application_status == "Selected"
    ).all()


def rejected_candidates(db: Session):

    return db.query(models.Candidate).filter(
        models.Candidate.application_status == "Rejected"
    ).all()