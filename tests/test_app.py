import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_for_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser1@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity_name}" in response.json().get("message", "")
    # Clean up: Remove test user
    client.delete(f"/activities/{activity_name}/participants/{email}")

def test_signup_duplicate():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser2@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.delete(f"/activities/{activity_name}/participants/{email}")

def test_remove_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser3@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity_name}" in response.json().get("message", "")

def test_remove_nonexistent_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@example.com"
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")
