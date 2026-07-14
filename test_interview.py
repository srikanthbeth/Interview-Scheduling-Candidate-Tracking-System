def create_interviewer(test_client):

    # Register Interviewer
    test_client.post(
        "/auth/register",
        json={
            "name": "Interviewer",
            "email": "interviewer1@test.com",
            "password": "interviewer123",
            "role": "Interviewer"
        }
    )

    # Login Interviewer
    login = test_client.post(
        "/auth/login",
        data={
            "username": "interviewer1@test.com",
            "password": "interviewer123"
        }
    )

    token = login.json()["access_token"]

    return token


import uuid


def create_candidate(test_client, token):

    email = f"{uuid.uuid4().hex[:8]}@test.com"

    response = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Rahul",
            "email": email,
            "phone": "9876543210",
            "experience": 3,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    assert response.status_code == 200

    return response.json()["id"]


import uuid


def get_interviewer_id(test_client):

    email = f"{uuid.uuid4().hex[:8]}@test.com"

    response = test_client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": email,
            "password": "john123",
            "role": "Interviewer"
        }
    )

    return response.json()["id"]


def create_interview(test_client, admin_token):

    candidate_id = create_candidate(test_client, admin_token)

    interviewer_id = get_interviewer_id(test_client)

    response = test_client.post(
        "/interviews/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "candidate_id": candidate_id,
            "interviewer_id": interviewer_id,
            "interview_date": "2026-07-20",
            "interview_time": "10:30:00",
            "interview_mode": "Online",
            "status": "Scheduled"
        }
    )

    return response


# -----------------------------
# Create Interview
# -----------------------------
def test_create_interview(test_client, admin_token):

    response = create_interview(test_client, admin_token)

    assert response.status_code == 200
    assert response.json()["status"] == "Scheduled"


# -----------------------------
# Get Interviews
# -----------------------------
def test_get_interviews(test_client, admin_token):

    create_interview(test_client, admin_token)

    response = test_client.get(
        "/interviews/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------------
# Get Interview By ID
# -----------------------------
def test_get_interview_by_id(test_client, admin_token):

    interview = create_interview(test_client, admin_token)

    interview_id = interview.json()["id"]

    response = test_client.get(
        f"/interviews/{interview_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == interview_id


# -----------------------------
# Update Interview
# -----------------------------
def test_update_interview(test_client, admin_token):

    interview = create_interview(test_client, admin_token)

    interview_id = interview.json()["id"]

    response = test_client.put(
        f"/interviews/{interview_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "candidate_id": interview.json()["candidate_id"],
            "interviewer_id": interview.json()["interviewer_id"],
            "interview_date": "2026-07-20",
            "interview_time": "10:30:00",
            "interview_mode": "Offline",
            "status": "Completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


# -----------------------------
# Duplicate Interview
# -----------------------------
def test_duplicate_interview(test_client, admin_token):

    # Create Candidate
    candidate = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Duplicate Candidate",
            "email": "duplicatecandidate@test.com",
            "phone": "9876543210",
            "experience": 3,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    candidate_id = candidate.json()["id"]

    # Register Interviewer
    interviewer = test_client.post(
        "/auth/register",
        json={
            "name": "Duplicate Interviewer",
            "email": "duplicateinterviewer@test.com",
            "password": "password123",
            "role": "Interviewer"
        }
    )

    interviewer_id = interviewer.json()["id"]

    payload = {
        "candidate_id": candidate_id,
        "interviewer_id": interviewer_id,
        "interview_date": "2026-07-20",
        "interview_time": "10:30:00",
        "interview_mode": "Online",
        "status": "Scheduled"
    }

    # First interview
    response1 = test_client.post(
        "/interviews/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    assert response1.status_code == 200

    # Duplicate interview (same interviewer, same date & time)
    response2 = test_client.post(
        "/interviews/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    assert response2.status_code == 400
    assert response2.json()["detail"] == (
        "Interview already scheduled for this interviewer at the selected date and time."
    )

# -----------------------------
# Interviewer Cannot Create Interview
# -----------------------------
def test_interviewer_cannot_create_interview(
    test_client,
    interviewer_token
):

    response = test_client.post(
        "/interviews/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json={
            "candidate_id": 1,
            "interviewer_id": 1,
            "interview_date": "2026-07-20",
            "interview_time": "10:30:00",
            "interview_mode": "Online",
            "status": "Scheduled"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"