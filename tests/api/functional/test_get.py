from datetime import date

from app import db
from app.models import Response, UserGroup, Participant
from flask.helpers import url_for
from tests.helpers import (
    api_login,
    create_card,
    create_admin,
    create_participant,
    create_study,
    create_user_group,
    create_data_value_label,
    create_card_set,
    create_cards,
    create_response,
)
from app.api.helpers import (
    create_card_json,
    create_card_set_json,
    create_data_value_label_json,
    create_card_position_json,
    create_data_value_json
)


def test_get_no_access_token(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/api/get/*' is requested with no access token (GET)
    THEN check response code, and content
    """

    with client.application.test_request_context():
        response = client.get(url_for("api.get_response", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_responses"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_participant", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_participants"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_user_group", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_user_groups"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_data_value_label", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_data_value_labels"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_study", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_studies"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_card_set", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_card_sets"))
        assert response.status_code == 401
        response = client.get(url_for("api.get_card", id=1))
        assert response.status_code == 401
        response = client.get(url_for("api.get_all_cards"))
        assert response.status_code == 401


def test_get_individual_response(client, init_database):
    """
    GIVEN a Flask application and a logged in admin
    WHEN '/api/get/response/1' is requested with valid access token (GET)
    THEN check response code, and content
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)
        study = create_study(client, creator=admin)
        study_response = create_response(client, creator=admin, study=study, participant=study.user_group.users[0])

        response = client.get(
            url_for("api.get_response", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        assert response.status_code == 200

        json = response.json
        assert json["id"] == study_response.id
        assert json["study_id"] == study_response.study_id
        assert json["participant_id"] == study_response.participant_id
        assert json["card_positions"] == [create_card_position_json(card_position) for card_position in study_response.card_positions]
        assert json["data_values"] == [create_data_value_json(data_value) for data_value in study_response.data_values]


def test_get_all_responses(client, init_database):
    """
    GIVEN a Flask application and logged in user
    WHEN '/api/get/response/all' is requested with valid access token (GET)
    THEN check status code and response content and length
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)
        participant_1 = create_participant(client, username="p1")
        participant_2 = create_participant(client, username="p2")
        user_group = create_user_group(client, participants=[participant_1, participant_2], creator=admin)
        study = create_study(client, creator=admin, user_group=user_group)
        study_response_1 = create_response(
            client, creator=admin, participant=participant_1, study=study
        )
        study_response_2 = create_response(
            client, creator=admin, participant=participant_2, study=study
        )

        response = client.get(
            url_for("api.get_all_responses"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )
        assert response.status_code == 200
        assert len(response.json) == 2


def test_get_individual_participant(client, init_database):
    """
    GIVEN a Flask application and a logged in admin
    WHEN '/api/get/participant/1' is requested with valid access token (GET)
    THEN check response code, and content
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        participant = create_participant(client)
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )

        response = client.get(
            url_for("api.get_participant", id=2),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert json["id"] == participant.id
        assert json["username"] == participant.username
        assert json["type"] == participant.type


def test_get_all_participants(client, init_database):
    """
    GIVEN a Flask application and a logged in admin
    WHEN '/api/get/participant/all' is requested with valid access token (GET)
    THEN check response code, and content
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        participant_1 = create_participant(client, username="p1")
        participant_2 = create_participant(client, username="p2")
        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )

        response = client.get(
            url_for("api.get_all_participants"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert len(json) == 2
        assert json[0]["id"] == participant_1.id
        assert json[0]["username"] == participant_1.username
        assert json[0]["type"] == participant_1.type
        assert json[1]["id"] == participant_2.id
        assert json[1]["username"] == participant_2.username
        assert json[1]["type"] == participant_2.type


def test_get_individual_user_group(client, init_database):
    """
    GIVEN a Flask application and a logged in admin
    WHEN '/api/get/user_group/1' is requested with a valid access token (GET)
    THEN check response code and content
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        participant_1 = create_participant(client, username="p1")
        participant_2 = create_participant(client, username="p2")
        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )

        response = client.get(
            url_for("api.get_user_group", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )
        json = response.json

        assert response.status_code == 200
        assert json["id"] == user_group.id
        assert json["name"] == user_group.name


def test_get_all_user_groups(client, init_database):
    """
    GIVEN a Flask application and a logged in admin
    WHEN '/api/get/user_group/all' is requested with a valid access token (GET)
    THEN check response code and content
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        participant_1 = create_participant(client, username="p1")
        participant_2 = create_participant(client, username="p2")
        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )

        participant_1 = create_participant(client, username="p3")
        participant_2 = create_participant(client, username="p4")
        user_group = create_user_group(
            client, creator=admin, participants=[participant_1, participant_2]
        )

        response = client.get(
            url_for("api.get_all_user_groups"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert len(json) == 2


def test_get_indvidual_data_value_label(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a data value label created
    WHEN '/api/get/data_value_label/1' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        data_value_label = create_data_value_label(client, creator=admin)
        response = client.get(
            url_for("api.get_data_value_label", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert json["id"] == data_value_label.id
        assert json["label"] == data_value_label.label


def test_get_all_data_value_label(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a data value label created
    WHEN '/api/get/data_value_label/all' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        data_value_label_1 = create_data_value_label(client, creator=admin)
        data_value_label_2 = create_data_value_label(client, creator=admin)

        response = client.get(
            url_for("api.get_all_data_value_labels"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert json[0]["id"] == data_value_label_1.id
        assert json[0]["label"] == data_value_label_1.label
        assert json[1]["id"] == data_value_label_2.id
        assert json[1]["label"] == data_value_label_2.label


def test_get_individual_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a study created
    WHEN '/api/get/study/1' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        study = create_study(client, creator=admin)
        response = client.get(
            url_for("api.get_study", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert json["id"] == study.id
        assert json["name"] == study.name
        assert json["description"] == study.description
        assert json["image"] == study.image
        assert json["card_set_x"] == create_card_set_json(study.card_set_x)
        assert json["card_set_y"] == create_card_set_json(study.card_set_y)
        assert json["data_value_labels"] == [
            create_data_value_label_json(data_value_label)
            for data_value_label in study.data_value_labels
        ]
        assert json["number_of_columns"] == study.number_of_columns
        assert json["number_of_rows"] == study.number_of_rows
        assert json["user_group_id"] == study.user_group.id


def test_get_all_studies(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a study created
    WHEN '/api/get/study/all' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        p1 = create_participant(client, username="p1")
        p2 = create_participant(client, username="p2")
        ug1 = create_user_group(client, participants=[p1], creator=admin)
        ug2 = create_user_group(client, participants=[p2], creator=admin)
        study_1 = create_study(client, creator=admin, user_group=ug1)
        study_2 = create_study(client, creator=admin, user_group=ug2)
        response = client.get(
            url_for("api.get_all_studies"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        json = response.json

        assert response.status_code == 200
        assert len(json) == 2


def test_get_individual_cards(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a card set created
    WHEN '/api/get/card/1' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        card = create_card(client, creator=admin)

        response = client.get(
            url_for("api.get_card", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        assert response.status_code == 200

        json = response.json
        assert json["id"] == card.id
        assert json["name"] == card.name
        assert json["description"] == card.description
        assert json["image"] == card.image


def test_get_all_cards(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a card set created
    WHEN '/api/get/card/all' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        cards_1 = create_card(client, creator=admin)
        cards_2 = create_card(client, creator=admin)

        response = client.get(
            url_for("api.get_all_cards"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        assert response.status_code == 200

        json = response.json
        assert len(json) == 2
        assert json[0]["id"] == cards_1.id
        assert json[0]["name"] == cards_1.name
        assert json[0]["description"] == cards_1.description
        assert json[0]["image"] == cards_1.image
        assert json[1]["id"] == cards_2.id
        assert json[1]["name"] == cards_2.name
        assert json[1]["description"] == cards_2.description
        assert json[1]["image"] == cards_2.image


def test_get_individual_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a card set created
    WHEN '/api/get/card_set/1' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        card_set = create_card_set(client, creator=admin)

        response = client.get(
            url_for("api.get_card_set", id=1),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        assert response.status_code == 200

        json = response.json
        assert json["id"] == card_set.id
        assert json["name"] == card_set.name
        assert json["measure"] == card_set.measure


def test_get_all_card_sets(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a card set created
    WHEN '/api/get/card_set/all' is requested with a valid access token (GET)
    THEN check response is valid, and content is correct.
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        access_token = api_login(client)

        card_set_1 = create_card_set(client, creator=admin)
        card_set_2 = create_card_set(client, creator=admin)

        response = client.get(
            url_for("api.get_all_card_sets"),
            headers={
                "Authorization": "Bearer {}".format(
                    access_token["access_token"]
                )
            },
        )

        assert response.status_code == 200

        json = response.json
        assert len(json) == 2
        assert json[0]["id"] == card_set_1.id
        assert json[0]["name"] == card_set_1.name
        assert json[0]["measure"] == card_set_1.measure
        assert json[1]["id"] == card_set_2.id
        assert json[1]["name"] == card_set_2.name
        assert json[1]["measure"] == card_set_2.measure
