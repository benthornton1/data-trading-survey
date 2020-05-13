from urllib.parse import urlparse

from flask import url_for

from tests.helpers import (
    login,
    create_participant,
    create_study,
    create_user_group,
    create_admin,
    create_response,
)


def test_get_general_study(client, init_database):
    """
    GIVEN a Flask application, admin, study, responses
    WHEN '/responses/<int:id>' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(
            client,
            username="participant",
            password="password",
            gender="Male",
            age_group="20-29",
            country_of_birth="AF",
            latest_country="AX",
            education_level="L6",
            occupation="Almoner",
            completed_form=True,
        )

        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)
        study_response = create_response(
            client, participant=participant, creator=admin, study=study
        )
        
        login(client, username="admin", password="password")

        response = client.get(
            url_for("responses.general", id=study.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert (
            bytes(str(len(study.responses)) + " Responses", "utf-8")
            in response.data
        )
        

        client.get(url_for("auth.logout"))
        admin2 = create_admin(client, username="admin2", password="password")
        login(client, username="admin2", password="password")

        response = client.get(
            url_for("responses.general", id=study.id), follow_redirects=False
        )

        assert urlparse(response.location).path == url_for("auth.login")


def test_get_general_no_study(client, init_database):
    """
    GIVEN a Flask application, admin
    WHEN '/responses/1' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client)

        login(client, username="admin", password="password")

        response = client.get(
            url_for("responses.general", id=1), follow_redirects=True
        )

        assert response.status_code == 404
