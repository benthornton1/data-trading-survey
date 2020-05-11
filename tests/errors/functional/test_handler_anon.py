from flask import url_for


def test_anonymous_error_handler_404(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/<path:unkown_path>' is requested (GET)
    THEN check response content, status code
    """

    with client.application.test_request_context():
        response = client.get("/no_resource_found_here", follow_redirects=True)

        assert response.status_code == 404
        assert b"Error :(" in response.data
        assert b"404 Not Found" in response.data
        assert b"Go Back" in response.data
        assert bytes(url_for("auth.login"), "utf-8") in response.data


def test_anonymous_error_handler_405(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/logout' is posted (POST)
    THEN check response content, status code
    """

    with client.application.test_request_context():
        response = client.post(url_for("auth.logout"), follow_redirects=True)

        assert response.status_code == 405
        assert b"Error :(" in response.data
        assert b"405 Method Not Allowed" in response.data
        assert b"Go Back" in response.data
        assert bytes(url_for("auth.login"), "utf-8") in response.data
