"""Tests for GET /activities endpoint"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activity_count = 9
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Volleyball Club",
        "Art Studio",
        "Music Ensemble",
        "Debate Team",
        "STEM Research Club"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == expected_activity_count
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_structure(client):
    """Test that each activity has the correct structure"""
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict), f"Activity {activity_name} is not a dict"
        assert required_keys.issubset(activity_data.keys()), \
            f"Activity {activity_name} missing required keys"
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_has_participants(client):
    """Test that activities have initial participants"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert activity_name in activities
    assert len(activities[activity_name]["participants"]) > 0
    assert all(isinstance(email, str) for email in activities[activity_name]["participants"])
