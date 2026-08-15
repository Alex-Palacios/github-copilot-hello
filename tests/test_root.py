"""Tests for GET / endpoint"""
import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html"""
    # Arrange
    # No arrange needed for this simple test

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in [301, 302, 303, 307, 308]  # Common redirect status codes
    assert "location" in response.headers
    assert "/static/index.html" in response.headers["location"]


def test_root_with_follow_redirects(client):
    """Test that GET / redirect ultimately serves the index page"""
    # Arrange
    # No arrange needed

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    # Should contain HTML content
    assert "text/html" in response.headers.get("content-type", "")
