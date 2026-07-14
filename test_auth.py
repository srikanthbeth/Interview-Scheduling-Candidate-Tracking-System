def test_register_admin(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "name": "Admin",
            "email": "admin1@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "admin1@test.com"
    assert response.json()["role"] == "Admin"


def test_duplicate_email(test_client):

    user = {
        "name": "HR",
        "email": "duplicate@test.com",
        "password": "hr123",
        "role": "HR"
    }

    test_client.post("/auth/register", json=user)

    response = test_client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(test_client):

    test_client.post(
        "/auth/register",
        json={
            "name": "Interviewer",
            "email": "login@test.com",
            "password": "test123",
            "role": "Interviewer"
        }
    )

    response = test_client.post(
        "/auth/login",
        data={
            "username": "login@test.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(test_client):

    response = test_client.post(
        "/auth/login",
        data={
            "username": "wrong@test.com",
            "password": "wrong123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"