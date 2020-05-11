from flask import url_for

from tests.helpers import create_admin, create_participant, login


def test_admin_error_handler_404(client, init_database):
    """
    GIVEN a Flask application, logged in admin
    WHEN '/<path:unkown_path>' is requested (GET)
    THEN check response content, status code
    """

    with client.application.test_request_context():
        create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        response = client.get("/no_resource_found_here", follow_redirects=True)

        assert response.status_code == 404
        assert b"Error :(" in response.data
        assert b"404 Not Found" in response.data
        assert b"Go Back" in response.data
        assert bytes(url_for("admin.index"), "utf-8") in response.data
        client.get(url_for("auth.logout"))


def test_admin_error_handler_405(client, init_database):
    """
    GIVEN a Flask application, logged in admin
    WHEN '/index' is POSTED (POST)
    THEN check response content, status code
    """

    with client.application.test_request_context():
        create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        response = client.post(url_for("admin.index"), follow_redirects=True)

        assert response.status_code == 405
        assert b"Error :(" in response.data
        assert b"405 Method Not Allowed" in response.data
        assert b"Go Back" in response.data
        assert bytes(url_for("admin.index"), "utf-8") in response.data
        client.get(url_for("auth.logout"))
