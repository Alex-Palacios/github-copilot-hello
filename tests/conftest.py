"""Shared fixtures for API tests"""
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app


# Store the original activities on module load
def _get_fresh_activities():
    """Get a fresh copy of the original activities"""
    from src.app import activities
    return deepcopy(activities)


# Capture original state once
_ORIGINAL_ACTIVITIES = _get_fresh_activities()


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset activities to fresh state before and after each test.
    This ensures complete data isolation between tests.
    """
    from src.app import activities
    
    # Deep copy the original state to restore before test
    fresh_state = deepcopy(_ORIGINAL_ACTIVITIES)
    
    # Clear all activities and restore from fresh copy
    activities.clear()
    for key, value in fresh_state.items():
        activities[key] = deepcopy(value)
    
    yield
    
    # Restore again after test
    activities.clear()
    for key, value in fresh_state.items():
        activities[key] = deepcopy(value)
