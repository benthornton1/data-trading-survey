from statistics import mean
from urllib.parse import urlparse

from flask import url_for
from munch import munchify

from tests.helpers import (
    login,
    create_participant,
    create_study,
    create_user_group,
    create_admin,
    create_response,
)


def test_get_compare_responses(client, init_database):
    """
    GIVEN a Flask application, admin, study, responses
    WHEN '/responses/compare_responses/<int:id>' is requested (GET)
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
            url_for("responses.compare_responses", id=study.id),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Compare Responses" in response.data
        assert (
            bytes(
                "Here you can compare responses to study <b>{}</b> from pairs of users.".format(
                    study.name
                ),
                "utf-8",
            )
            in response.data
        )
        assert b"Response 1" in response.data
        assert b"Response 2" in response.data
        assert b"Average" in response.data
        assert bytes(str(participant_1.username), "utf-8") in response.data
        assert bytes(str(participant_2.username), "utf-8") in response.data

        client.get(url_for("auth.logout"))
        admin2 = create_admin(client, username="admin2", password="password")
        login(client, username="admin2", password="password")

        response = client.get(
            url_for("responses.compare_responses", id=study.id),
            follow_redirects=False,
        )

        assert urlparse(response.location).path == url_for("auth.login")


def test_post_compare_responses(client, init_database):
    """
    GIVEN a Flask application, admin, study, responses
    WHEN '/responses/compare_responses/<int:id>' is posted (POST)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client)

        participant_1 = create_participant(
            client,
            username="p1",
            password="password",
            gender="Male",
            age_group="20-29",
            country_of_birth="AF",
            latest_country="AX",
            education_level="L6",
            occupation="Almoner",
            completed_form=True,
        )
        participant_2 = create_participant(client, username="p2")

        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )
        study = create_study(client, creator=admin, user_group=user_group)
        study_response_1 = create_response(
            client, participant=participant_2, creator=admin, study=study
        )
        study_response_2 = create_response(
            client, participant=participant_2, creator=admin, study=study
        )

        login(client, username="admin", password="password")

        data = {
            "response_id_1": study_response_1.id,
            "response_id_2": study_response_2.id,
        }

        response = client.post(
            url_for("responses.compare_responses", id=study.id),
            json=data,
            follow_redirects=True,
        )
        
        for data_value in study_response_1.data_values:
            assert bytes(data_value.data_value_label.label, 'utf-8') in response.data
            assert bytes(str(data_value.value), 'utf-8') in response.data
           
        for data_value in study_response_2.data_values:
            assert bytes(data_value.data_value_label.label, 'utf-8') in response.data
            assert bytes(str(data_value.value), 'utf-8') in response.data
