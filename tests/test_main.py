import pytest

def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_assignment_not_logged_in(client):
    response = client.get('/assignment')
    assert response.status_code == 302  # Assumes a redirect to the login page when not logged in

def test_profile_not_logged_in(client):
    response = client.get('/profile')
    assert response.status_code == 302  # Assumes a redirect to the login page when not logged in

def test_routes_when_logged_in(client, auth):
    # Log in
    auth.login()

    with client:
        # Test home page
        response = client.get('/home')
        assert response.status_code == 200

        # Test assignment page
        response = client.get('/assignment')
        assert response.status_code == 200

        # Test profile page
        response = client.get('/profile')
        assert response.status_code == 200