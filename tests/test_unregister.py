"""Tests for POST /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"  # Already in Chess Club
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    assert email_to_remove in initial_response.json()[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email_to_remove}
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email_to_remove in result["message"]
    assert activity_name in result["message"]

    # Verify participant was removed
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count - 1
    assert email_to_remove not in updated_response.json()[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister fails for non-existent activity"""
    # Arrange
    fake_activity = "Fake Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{fake_activity}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_student_not_registered(client):
    """Test unregister fails if student is not registered"""
    # Arrange
    activity_name = "Chess Club"
    non_registered_email = "notregistered@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": non_registered_email}
    )

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_missing_email_parameter(client):
    """Test unregister fails if email parameter is missing"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister")

    # Assert
    assert response.status_code == 422  # Validation error


def test_unregister_multiple_participants(client):
    """Test removing multiple participants from same activity"""
    # Arrange
    activity_name = "Chess Club"
    emails_to_remove = ["michael@mergington.edu", "daniel@mergington.edu"]
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    for email in emails_to_remove:
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200

    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count - len(emails_to_remove)
    for email in emails_to_remove:
        assert email not in final_response.json()[activity_name]["participants"]


def test_signup_then_unregister_same_student(client):
    """Test signup followed by unregister for same student"""
    # Arrange
    activity_name = "Art Studio"
    email = "testuser@mergington.edu"

    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200

    # Verify signed up
    after_signup = client.get("/activities").json()
    assert email in after_signup[activity_name]["participants"]
    signup_count = len(after_signup[activity_name]["participants"])

    # Act - Unregister
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200

    # Assert - Verify unregistered
    after_unregister = client.get("/activities").json()
    assert email not in after_unregister[activity_name]["participants"]
    assert len(after_unregister[activity_name]["participants"]) == signup_count - 1
