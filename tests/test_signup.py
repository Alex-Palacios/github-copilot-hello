"""Tests for POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert new_email in result["message"]
    assert activity_name in result["message"]

    # Verify participant was added
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count + 1
    assert new_email in updated_response.json()[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test signup fails for non-existent activity"""
    # Arrange
    fake_activity = "Fake Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_already_registered(client):
    """Test signup fails if student already registered"""
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club participants

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_missing_email_parameter(client):
    """Test signup fails if email parameter is missing"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422  # Validation error


def test_signup_multiple_students(client):
    """Test multiple students can sign up for same activity"""
    # Arrange
    activity_name = "Programming Class"
    emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    for email in emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count + len(emails)
    for email in emails:
        assert email in final_response.json()[activity_name]["participants"]


def test_signup_different_activities(client):
    """Test student can sign up for multiple different activities"""
    # Arrange
    student_email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Art Studio", "Music Ensemble"]

    # Act
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        assert response.status_code == 200

    # Assert
    final_response = client.get("/activities")
    all_activities = final_response.json()
    for activity_name in activities_to_join:
        assert student_email in all_activities[activity_name]["participants"]
