import pytest
from MUSQL.utils import data_loading

def test_load_assignment_data():
    assignments = data_loading.load_assignment_data()

    # Check if the returned data is a list and not empty
    assert isinstance(assignments, list)
    assert len(assignments) > 0

    # Check if the returned assignments have the expected keys
    expected_keys = ['title', 'context', 'notice', 'max_attempts', 'assignment_number', 'date', 'duration']
    for assignment in assignments:
        assert all(key in assignment for key in expected_keys)

def test_load_user_data():
    # Load user data for an existing user
    user = data_loading.load_user_data("test")
    assert user is not None
    assert user['username'] == "test"

    # Load user data for a non-existing user
    non_existent_user = data_loading.load_user_data("non_existent_user")
    assert non_existent_user is None

