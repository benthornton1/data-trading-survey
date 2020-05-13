import ast
from urllib.parse import urlparse

from flask import url_for

from app.models import Response
from tests.helpers import (
    login,
    create_admin,
    create_participant,
    create_study,
    create_user_group,
)

from munch import munchify


def test_get_study(client, init_database):
    """
    GIVEN a Flask application, participant, study
    WHEN '/study/<int:id>' is requested (GET)
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

        login(client, username="participant", password="password")

        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=True
        )
        no_rows = str(study.number_of_rows - 1)
        no_cols = str(study.number_of_columns - 1)
        assert response.status_code == 200

        assert bytes(study.card_set_x.name, "utf-8") in response.data
        assert bytes(study.card_set_x.cards[0].name, "utf-8") in response.data
        assert (
            bytes(study.card_set_x.cards[0].description, "utf-8")
            in response.data
        )
        assert bytes(study.card_set_x.cards[0].image, "utf-8") in response.data
        assert (
            bytes("Highest " + study.card_set_x.measure, "utf-8")
            in response.data
        )
        assert (
            bytes("Lowest " + study.card_set_x.measure, "utf-8")
            in response.data
        )

        assert bytes(study.card_set_y.name, "utf-8") in response.data
        assert bytes(study.card_set_y.cards[0].name, "utf-8") in response.data
        assert (
            bytes(study.card_set_y.cards[0].description, "utf-8")
            in response.data
        )
        assert bytes(study.card_set_y.cards[0].image, "utf-8") in response.data
        assert (
            bytes("Highest " + study.card_set_y.measure, "utf-8")
            in response.data
        )
        assert (
            bytes("Lowest " + study.card_set_y.measure, "utf-8")
            in response.data
        )

        assert (
            bytes(study.data_value_labels[0].label, "utf-8") in response.data
        )

        assert bytes("row_" + no_rows, "utf-8") in response.data
        assert bytes("col_" + no_cols, "utf-8") in response.data


def test_post_study(client, init_database):
    """
    GIVEN a Flask application, participant, study
    WHEN '/study/<int:id>' is posted (POST)
    THEN check database content, status code, response content
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

        cards_x = {
            "col_0": [
                {
                    "id": 10,
                    "name": "Financial",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 8,
                    "name": "Fashion",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 11,
                    "name": "Food and Beverage",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 7,
                    "name": "GP Health Records",
                    "image": "yay.jpg",
                    "description": "",
                },
            ],
            "col_1": [
                {
                    "id": 9,
                    "name": "Communications",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 6,
                    "name": "Service Contracts",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 12,
                    "name": "Location",
                    "image": "yay.jpg",
                    "description": "",
                },
            ],
            "col_2": [
                {
                    "id": 4,
                    "name": "Demographics Data",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 3,
                    "name": "Activity and Sleep",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 5,
                    "name": "Household",
                    "image": "yay.jpg",
                    "description": "",
                },
            ],
            "col_3": [
                {
                    "id": 1,
                    "name": "Entertainment",
                    "image": "yay.jpg",
                    "description": "",
                },
                {
                    "id": 2,
                    "name": "Sensitive Health Report",
                    "image": "yay.jpg",
                    "description": "",
                },
            ],
        }
        cards_y = {
            "row_3": [
                {
                    "id": 18,
                    "name": "Government Regulated",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 13,
                    "name": "Mortgage",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 25,
                    "name": "Banks",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 22,
                    "name": "Supermarket",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 15,
                    "name": "Products and Services",
                    "image": "hi.jpg",
                    "description": "",
                },
            ],
            "row_2": [
                {
                    "id": 16,
                    "name": "Insurance",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 14,
                    "name": "Research Institute",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 27,
                    "name": "Electricity",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 26,
                    "name": "Government",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 24,
                    "name": "Council",
                    "image": "hi.jpg",
                    "description": "",
                },
            ],
            "row_1": [
                {
                    "id": 20,
                    "name": "Health Service",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 21,
                    "name": "Religious Organisation",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 17,
                    "name": "Education Institute",
                    "image": "hi.jpg",
                    "description": "",
                },
            ],
            "row_0": [
                {
                    "id": 19,
                    "name": "Social Media",
                    "image": "hi.jpg",
                    "description": "",
                },
                {
                    "id": 23,
                    "name": "Authorities",
                    "image": "hi.jpg",
                    "description": "",
                },
            ],
        }
        data_values = {
            "col_0_row_3": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 43,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 63,
                },
            ],
            "col_1_row_3": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 82,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 72,
                },
            ],
            "col_2_row_3": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 82,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 99,
                },
            ],
            "col_3_row_3": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 71,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 72,
                },
            ],
            "col_0_row_2": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 42,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 52,
                },
            ],
            "col_1_row_2": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 67,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 89,
                },
            ],
            "col_2_row_2": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 52,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 62,
                },
            ],
            "col_3_row_2": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 66,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 72,
                },
            ],
            "col_0_row_1": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 82,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 65,
                },
            ],
            "col_1_row_1": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 82,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 32,
                },
            ],
            "col_2_row_1": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 42,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 82,
                },
            ],
            "col_3_row_1": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 92,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 73,
                },
            ],
            "col_0_row_0": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 43,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 77,
                },
            ],
            "col_1_row_0": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 28,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 32,
                },
            ],
            "col_2_row_0": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 12,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 44,
                },
            ],
            "col_3_row_0": [
                {
                    "id": 1,
                    "label": "You get the benefit (e.g. Personalised Service)",
                    "value": 66,
                },
                {
                    "id": 2,
                    "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                    "value": 34,
                },
            ],
        }
        data = {
            "cards_x": cards_x,
            "cards_y": cards_y,
            "data_values": data_values,
        }

        login(client, username="participant", password="password")

        response = client.post(
            url_for("study.study", id=study.id),
            json=dict(data),
            follow_redirects=False,
        )
        response_data_json = ast.literal_eval(response.data.decode("utf-8"))
        assert response_data_json["url"] == url_for("study.complete")

        response = client.get(response_data_json["url"], follow_redirects=True)

        assert response.status_code == 200
        assert b"Thank You!" in response.data
        assert (
            b"<p>Thanks for participating in the study, you can now log out of the system.</p>"
            in response.data
        )

        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")

        response = client.get(url_for("study.index"), follow_redirects=False)
        assert urlparse(response.location).path == url_for("study.complete")

        response = client.get(
            url_for("study.change_info"), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")

        response = client.get(
            url_for("study.user_info"), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")

        response_db = Response.query.filter_by(
            participant=participant
        ).first()

        assert response_db.study == study
        assert response_db.participant == participant
        
        cards_x_munch = munchify(cards_x)
        cards_y_munch = munchify(cards_y)   
        data_values_munch = munchify(data_values)

        for col, cards in cards_x_munch.items():
            col_num = int(col.split('_')[1])
            for card in cards:
                for card_position in response_db.card_positions:
                    if card == card_position.card:
                        assert card_position.col == col_num
                        

        for row, cards in cards_y_munch.items():
            
            row_num = int(row.split('_')[1])
            for card in cards:
                for card_position in response_db.card_positions:
                    if card == card_position.card:
                        assert card_position.row_num == row_num
                
        for col_row, data_values in data_values_munch.items():
            col_num = int(col_row.split('_')[1])
            row_num = int(col_row.split('_')[3])
            
            for data_value in data_values:
                for data_value_db in response_db.data_values:
                    if col_num == data_value_db.column and row_num == data_value_db.row and data_value_db.data_value_label.label == data_value.label:
                        assert data_value_db.value == data_value.value
