# tests/conftest.py
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.db.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    app.state.redis = AsyncMock()
    client = TestClient(app)
    yield client



headers = {"X-API-KEY": settings.API_KEY} 

def test_register_user(client):
    # Data to be sent for user registration
    user_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    }

    response = client.post("/users/register/email-password", json=user_data, headers=headers)
    assert response.status_code == 200  
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"
    assert "id" in data 

