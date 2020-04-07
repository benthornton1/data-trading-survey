
from flask import url_for

from tests.helpers import create_admin

def test_valid_login(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/login' is posted with VALID credentials (POST)
    THEN check response is valid and user is logged in
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='IoTData')
        response = client.post(url_for('auth.login'),
                                    data=dict(username='admin', password='IoTData'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert b"Hello, admin" in response.data
        assert b"Logout" in response.data
        assert b"Login" not in response.data
        assert b"IoT Data Trading Survey Admin Site" in response.data

def test_logout_logged_in(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/logout' is requested when logged in (GET)
    THEN check response is valid and user is logged out
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='IoTData')
        # login
        response = client.post(url_for('auth.login'),
                                    data=dict(username='admin', password='IoTData'),
                                    follow_redirects=True)
        assert response.status_code == 200    
        # logout
        response = client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data
        assert b"Username" in response.data
        assert b"Password" in response.data
    
def test_logout_not_logged_in(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/logout' is requested when not logged in (GET)
    THEN check response is valid and user is logged out
    """
    with client.application.test_request_context():
        response = client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data
        assert b"Username" in response.data
        assert b"Password" in response.data