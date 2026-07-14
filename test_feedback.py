def create_completed_interview(test_client, admin_token):
    """
    Creates:
    Admin
        ↓
    Candidate
        ↓
    Interviewer
        ↓
    Completed Interview
    """

    # Create Candidate
    candidate = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Feedback Candidate",
            "email": "feedback@test.com",
            "phone": "9876543210",
            "experience": 2,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    candidate_id = candidate.json()["id"]

    # Register Interviewer
    interviewer = test_client.post(
        "/auth/register",
        json={
            "name": "Feedback Interviewer",
            "email": "feedbackinterviewer@test.com",
            "password": "password123",
            "role": "Interviewer"
        }
    )

    interviewer_id = interviewer.json()["id"]

    # Login Interviewer
    login = test_client.post(
        "/auth/login",
        data={
            "username": "feedbackinterviewer@test.com",
            "password": "password123"
        }
    )

    interviewer_token = login.json()["access_token"]

    # Create Interview
    interview = test_client.post(
        "/interviews/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "candidate_id": candidate_id,
            "interviewer_id": interviewer_id,
            "interview_date": "2026-07-25",
            "interview_time": "11:00:00",
            "interview_mode": "Online",
            "status": "Completed"
        }
    )

    return interview.json()["id"], interviewer_token


# -----------------------------------
# Submit Feedback
# -----------------------------------
def test_add_feedback(test_client, admin_token):

    interview_id, interviewer_token = create_completed_interview(
        test_client,
        admin_token
    )

    response = test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json={
            "interview_id": interview_id,
            "technical_rating": 5,
            "communication_rating": 4,
            "remarks": "Excellent Candidate"
        }
    )

    assert response.status_code == 200
    assert response.json()["technical_rating"] == 5


# -----------------------------------
# Get Feedback
# -----------------------------------
def test_get_feedback(test_client, admin_token):

    interview_id, interviewer_token = create_completed_interview(
        test_client,
        admin_token
    )

    test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json={
            "interview_id": interview_id,
            "technical_rating": 4,
            "communication_rating": 5,
            "remarks": "Good"
        }
    )

    response = test_client.get(
        f"/feedback/{interview_id}",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["remarks"] == "Good"


# -----------------------------------
# Duplicate Feedback
# -----------------------------------
def test_duplicate_feedback(test_client, admin_token):

    interview_id, interviewer_token = create_completed_interview(
        test_client,
        admin_token
    )

    payload = {
        "interview_id": interview_id,
        "technical_rating": 5,
        "communication_rating": 5,
        "remarks": "Excellent"
    }

    test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json=payload
    )

    response = test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Feedback already submitted"


# -----------------------------------
# Only Interviewer Can Submit Feedback
# -----------------------------------
def test_admin_cannot_submit_feedback(test_client, admin_token):

    response = test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "interview_id": 1,
            "technical_rating": 5,
            "communication_rating": 5,
            "remarks": "Test"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only Interviewer can submit feedback"


# -----------------------------------
# Feedback Before Completion
# -----------------------------------
def test_feedback_before_completion(test_client, admin_token):

    # Candidate
    candidate = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Before Completion",
            "email": "before@test.com",
            "phone": "9999999999",
            "experience": 2,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    candidate_id = candidate.json()["id"]

    # Interviewer
    interviewer = test_client.post(
        "/auth/register",
        json={
            "name": "Before",
            "email": "beforeinterviewer@test.com",
            "password": "password123",
            "role": "Interviewer"
        }
    )

    interviewer_id = interviewer.json()["id"]

    login = test_client.post(
        "/auth/login",
        data={
            "username": "beforeinterviewer@test.com",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    # Scheduled Interview
    interview = test_client.post(
        "/interviews/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "candidate_id": candidate_id,
            "interviewer_id": interviewer_id,
            "interview_date": "2026-08-01",
            "interview_time": "10:00:00",
            "interview_mode": "Online",
            "status": "Scheduled"
        }
    )

    interview_id = interview.json()["id"]

    response = test_client.post(
        "/feedback/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "interview_id": interview_id,
            "technical_rating": 5,
            "communication_rating": 5,
            "remarks": "Test"
        }
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Feedback can be added only after interview is completed"
    )