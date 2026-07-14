# Interview Scheduling & Candidate Tracking System

A FastAPI-based backend application for managing candidate hiring processes, interview scheduling, interviewer feedback, and recruitment reports with JWT Authentication and Role-Based Access Control.

---

## Features

### Authentication & Authorization
- JWT Authentication
- User Registration
- User Login
- Role-Based Access Control
- Roles:
  - Admin
  - HR
  - Interviewer

---

## Candidate Management

- Create Candidate
- View All Candidates
- View Candidate by ID
- Update Candidate Details
- Delete Candidate
- Update Candidate Status (HR Only)

Candidate Fields

- Name
- Email (Unique)
- Phone Number
- Experience
- Skill Set
- Application Status

---

## Interview Management

- Schedule Interview
- View Interviews
- View Interview by ID
- Update Interview

Interview Fields

- Candidate
- Interviewer
- Interview Date
- Interview Time
- Interview Mode
- Status

Interview Status

- Scheduled
- Completed
- Cancelled
- Selected
- Rejected

Business Rule

- Prevent duplicate interview schedules for the same interviewer on the same date and time.

---

## Feedback Management

- Add Interview Feedback
- View Interview Feedback

Feedback Fields

- Technical Rating
- Communication Rating
- Remarks

Business Rules

- Feedback can be submitted only after the interview is completed.
- Only the assigned interviewer can submit feedback.

---

## Reports

- Search Candidates by Skill Set
- Filter Interviews
- View Selected Candidates
- View Rejected Candidates
- Pagination Support

---

## Security

- JWT Authentication
- Password Hashing using Passlib (bcrypt)
- Role-Based Authorization

Permissions

### Admin

- Manage Users
- Manage Candidates
- Manage Interviews
- View Reports

### HR

- Manage Candidates
- Schedule Interviews
- Update Candidate Status
- View Reports

### Interviewer

- View Assigned Interviews
- Submit Feedback
- View Own Feedback

---

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Passlib
- bcrypt
- Python-Jose
- Pytest

---

## Project Structure

```
interview_scheduling_candidate_tracking_system/
│
├── routers/
│   ├── auth.py
│   ├── candidates.py
│   ├── interviews.py
│   ├── feedback.py
│   └── reports.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_candidate.py
│   ├── test_interview.py
│   ├── test_feedback.py
│   └── test_reports.py
│
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── models.py
├── schemas.py
├── utils.py
├── main.py
├── interview.db
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
```

### Move into Project

```bash
cd interview_scheduling_candidate_tracking_system
```

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Authentication APIs

### Register

```
POST /auth/register
```

### Login

```
POST /auth/login
```

---

## Candidate APIs

```
POST    /candidates/
GET     /candidates/
GET     /candidates/{id}
PUT     /candidates/{id}
PUT     /candidates/{id}/status
DELETE  /candidates/{id}
```

---

## Interview APIs

```
POST    /interviews/
GET     /interviews/
GET     /interviews/{id}
PUT     /interviews/{id}
```

---

## Feedback APIs

```
POST    /feedback/
GET     /feedback/{interview_id}
```

---

## Report APIs

```
GET /reports/search
GET /reports/interviews
GET /reports/selected
GET /reports/rejected
```

---

## Testing

Run all tests

```bash
pytest -v
```

Example Output

```
==========================
27 PASSED
==========================
```

---

## Validation

- Unique Email Validation
- Phone Number Validation
- JWT Token Validation
- Duplicate Interview Prevention
- Feedback Only After Interview Completion
- HR Only Can Update Candidate Status
- Interviewer Can Access Only Assigned Interviews

---

## Database

SQLite Database

```
interview.db
```

---

## Author

**Srikanth Bethamcharla**

---

## License

This project is developed for learning purposes as part of a FastAPI Backend Assignment.
