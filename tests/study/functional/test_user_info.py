from urllib.parse import urlparse

from flask import url_for

from app import db
from app.models import Participant
from app.study.forms import UserInfoForm
from tests.helpers import (
    login,
    create_admin,
    create_participant,
    create_study,
    create_user_group,
    create_data_value_label,
    create_card_set,
    create_cards,
    create_response,
    
)


def test_get_user_info(client, init_database):
    """
    GIVEN a Flask application, participant
    WHEN '/study/user_info' is requested (GET)
    THEN check response content, check they cant access any other page.
    """

    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(
            client, username="participant", password="password"
        )
        login(client, username="participant", password="password")

        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        response = client.get(
            url_for("study.user_info"), follow_redirects=True
        )
        form = UserInfoForm()
        assert response.status_code == 200
        assert b"Hi, participant" not in response.data
        assert bytes(form.gender.label.text, "utf-8") in response.data
        assert bytes(form.age_group.label.text, "utf-8") in response.data
        assert bytes(form.nationality.label.text, "utf-8") in response.data
        assert bytes(form.latest_country.label.text, "utf-8") in response.data
        assert bytes(form.education_level.label.text, "utf-8") in response.data
        assert bytes(form.occupation.label.text, "utf-8") in response.data
        assert bytes(form.income.label.text, "utf-8") in response.data


def test_post_user_info(client, init_database):

    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(
            client, username="participant", password="password"
        )
        login(client, username="participant", password="password")

        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        response = client.get(
            url_for("study.user_info"), follow_redirects=True
        )

        assert response.status_code == 200

        form = UserInfoForm()
        form.gender.data = "Male"
        form.age_group.data = "20-29"
        form.nationality.data = "AF"
        form.latest_country.data = "AX"
        form.education_level.data = "L6"
        form.occupation.data = "Almoner"
        form.income.data = "0-10000"
        form.submit.data = True

        repsonse = client.post(
            url_for("study.user_info"), data=form.data, follow_redirects=True
        )
        assert response.status_code == 200
        response = client.get(url_for("study.index"), follow_redirects=True)

        assert response.status_code == 200
        assert bytes(study.name, "utf-8") in response.data
        assert bytes(study.description, "utf-8") in response.data
        if study.image:
            assert bytes(study.image, "utf-8") in response.data
        else:
            assert b"study_images/no_image.jpg" in response.data

        participant_db = Participant.query.filter_by(id=participant.id).first()

        assert participant_db.gender == "Male"
        assert participant_db.age_group == "20-29"
        assert participant_db.country_of_birth == "AF"
        assert participant_db.latest_country == "AX"
        assert participant_db.education_level == "L6"
        assert participant_db.occupation == "Almoner"
        assert participant_db.completed_form == True
        assert participant_db.completed_study == False
