def create_candidate(test_client, token):
    response = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Rahul",
            "email": "rahul@test.com",
            "phone": "9876543210",
            "experience": 3,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    return response


# -----------------------------
# Create Candidate
# -----------------------------
def test_create_candidate(test_client, admin_token):

    response = create_candidate(test_client, admin_token)

    assert response.status_code == 200
    assert response.json()["name"] == "Rahul"
    assert response.json()["email"] == "rahul@test.com"


# -----------------------------
# Get All Candidates
# -----------------------------
def test_get_candidates(test_client, admin_token):

    create_candidate(test_client, admin_token)

    response = test_client.get(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------------
# Get Candidate By ID
# -----------------------------
def test_get_candidate_by_id(test_client, admin_token):

    create = create_candidate(test_client, admin_token)

    candidate_id = create.json()["id"]

    response = test_client.get(
        f"/candidates/{candidate_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == candidate_id


# -----------------------------
# Update Candidate
# -----------------------------
def test_update_candidate(test_client, admin_token):

    create = create_candidate(test_client, admin_token)

    candidate_id = create.json()["id"]

    response = test_client.put(
        f"/candidates/{candidate_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Rahul Updated",
            "email": "rahul@test.com",
            "phone": "9876543210",
            "experience": 5,
            "skill_set": "FastAPI",
            "application_status": "Applied"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Rahul Updated"


# -----------------------------
# Update Candidate Status
# -----------------------------
def test_update_candidate_status(test_client, hr_token):

    # Create candidate as HR
    response = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {hr_token}"
        },
        json={
            "name": "Kiran",
            "email": "kiran@test.com",
            "phone": "9999999999",
            "experience": 2,
            "skill_set": "Java",
            "application_status": "Applied"
        }
    )

    candidate_id = response.json()["id"]

    response = test_client.put(
        f"/candidates/{candidate_id}/status",
        headers={
            "Authorization": f"Bearer {hr_token}"
        },
        json={
            "application_status": "Selected"
        }
    )

    assert response.status_code == 200
    assert response.json()["application_status"] == "Selected"


# -----------------------------
# Delete Candidate
# -----------------------------
def test_delete_candidate(test_client, admin_token):

    create = create_candidate(test_client, admin_token)

    candidate_id = create.json()["id"]

    response = test_client.delete(
        f"/candidates/{candidate_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Candidate deleted successfully"


# -----------------------------
# Interviewer Cannot Create Candidate
# -----------------------------
def test_interviewer_cannot_create_candidate(
    test_client,
    interviewer_token
):

    response = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {interviewer_token}"
        },
        json={
            "name": "Test",
            "email": "test@test.com",
            "phone": "9876543210",
            "experience": 1,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"