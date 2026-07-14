def create_candidate(test_client, token, name, email, skill, status):

    response = test_client.post(
        "/candidates/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": name,
            "email": email,
            "phone": "9876543210",
            "experience": 2,
            "skill_set": skill,
            "application_status": status
        }
    )

    return response.json()


# ---------------------------------
# Search Candidate by Skill
# ---------------------------------

def test_search_candidate(test_client, admin_token):

    create_candidate(
        test_client,
        admin_token,
        "Rahul",
        "rahulpython@test.com",
        "Python",
        "Applied"
    )

    response = test_client.get(
        "/reports/search?skill=Python",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


# ---------------------------------
# Selected Candidates
# ---------------------------------

def test_selected_candidates(test_client, admin_token):

    create_candidate(
        test_client,
        admin_token,
        "Kiran",
        "selected@test.com",
        "Java",
        "Selected"
    )

    response = test_client.get(
        "/reports/selected",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert data[0]["application_status"] == "Selected"


# ---------------------------------
# Rejected Candidates
# ---------------------------------

def test_rejected_candidates(test_client, admin_token):

    create_candidate(
        test_client,
        admin_token,
        "Ramesh",
        "rejected@test.com",
        "Testing",
        "Rejected"
    )

    response = test_client.get(
        "/reports/rejected",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert data[0]["application_status"] == "Rejected"


# ---------------------------------
# Filter Interviews
# ---------------------------------

def test_filter_interviews(test_client, admin_token):

    response = test_client.get(
        "/reports/interviews?status=Scheduled",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------------------------------
# Unauthorized Access
# ---------------------------------

def test_reports_without_token(test_client):

    response = test_client.get(
        "/reports/selected"
    )

    assert response.status_code == 401