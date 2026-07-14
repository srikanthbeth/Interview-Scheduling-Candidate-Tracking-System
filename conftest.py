import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# -----------------------------
# Test Database
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_interview.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    database = TestingSessionLocal()

    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def test_client(db):
    yield client


# -----------------------------
# Register Users
# -----------------------------

@pytest.fixture
def admin_user(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "name": "Admin",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    return response.json()


@pytest.fixture
def hr_user(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "name": "HR",
            "email": "hr@test.com",
            "password": "hr123",
            "role": "HR"
        }
    )

    return response.json()


@pytest.fixture
def interviewer_user(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "name": "Interviewer",
            "email": "interviewer@test.com",
            "password": "interviewer123",
            "role": "Interviewer"
        }
    )

    return response.json()


# -----------------------------
# Login Tokens
# -----------------------------

@pytest.fixture
def admin_token(test_client, admin_user):

    response = test_client.post(
        "/auth/login",
        data={
            "username": "admin@test.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return token


@pytest.fixture
def hr_token(test_client, hr_user):

    response = test_client.post(
        "/auth/login",
        data={
            "username": "hr@test.com",
            "password": "hr123"
        }
    )

    token = response.json()["access_token"]

    return token


@pytest.fixture
def interviewer_token(test_client, interviewer_user):

    response = test_client.post(
        "/auth/login",
        data={
            "username": "interviewer@test.com",
            "password": "interviewer123"
        }
    )

    token = response.json()["access_token"]

    return token