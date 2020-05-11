from urllib.parse import urlparse

from flask import url_for

from tests.helpers import (
    create_admin,
    login,
    create_user_group,
    create_participant,
    create_response,
    create_study,
)


def test_get_create_pdf(client, init_database):
    """
    GIVEN a Flask application, admin, study, responses
    WHEN '/responses/create_pdf/<int:id>' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client)

        participant_1 = create_participant(client, username="p1")
        participant_2 = create_participant(client, username="p2")

        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )
        study = create_study(client, creator=admin, user_group=user_group)
        study_response_1 = create_response(
            client, participant=participant_1, creator=admin, study=study
        )
        study_response_2 = create_response(
            client, participant=participant_2, creator=admin, study=study
        )

        login(client, username="admin", password="password")

        response = client.get(
            url_for("responses.create_pdf", id=study.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Create PDF" in response.data
        assert (
            b"<p>Here you can generate a PDF and select what responses you want to include in the pdf</p>"
            in response.data
        )
        assert b"All Responses" in response.data
        assert b"Average Response" in response.data
        assert b"Specific Responses" in response.data
        assert bytes(str(participant_1.username), "utf-8") in response.data
        assert bytes(str(participant_2.username), "utf-8") in response.data

        client.get(url_for("auth.logout"))
        admin2 = create_admin(client, username="admin2", password="password")
        login(client, username="admin2", password="password")

        response = client.get(
            url_for("responses.create_pdf", id=study.id),
            follow_redirects=False,
        )

        assert urlparse(response.location).path == url_for("auth.login")
