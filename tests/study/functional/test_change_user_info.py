from flask import url_for

from app.models import Participant
from app.study.forms import UserInfoForm
from tests.helpers import (
    create_admin,
    create_participant,
    create_study,
    create_user_group,
    login,
)

from urllib.parse import urlparse


def test_get_change_user_info(client, init_database):
    """
    GIVEN a Flask application, participant, completed user_info form
    WHEN '/study/change_user_info' is requested (GET)
    THEN check status code and response content.
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

        login(client, username="participant", password="password")

        response = client.get(
            url_for("study.change_info"), follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Male" in response.data
        assert b"20-29" in response.data
        assert b"Afghanistan" in response.data
        assert b"Aland Islands" in response.data
        assert b"Level 6" in response.data
        assert b"Almoner" in response.data


def test_post_change_user_info(client, init_database):
    """
    GIVEN a Flask application, participant, completed user_info form
    WHEN '/study/change_user_info' is requested (GET)
    THEN check status code and response content.
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

        form = UserInfoForm()
        form.gender.data = "Prefer not to say"
        form.age_group.data = "60-69"
        form.nationality.data = "GB"
        form.latest_country.data = "GB"
        form.education_level.data = "L5"
        form.occupation.data = "Advertising Agent"
        form.income.data = "10000-20000"
        form.submit.data = True

        response = client.post(
            url_for("study.change_info"),
            data=form.data,
            follow_redirects=False,
        )

        assert urlparse(response.location).path == url_for("study.index")

        response = client.get(response.location, follow_redirects=True)

        assert response.status_code == 200

        participant_db = Participant.query.filter_by(id=participant.id).first()

        assert participant_db.gender == form.gender.data
        assert participant_db.age_group == form.age_group.data
        assert participant_db.country_of_birth == form.nationality.data
        assert participant_db.latest_country == form.latest_country.data
        assert participant_db.education_level == form.education_level.data
        assert participant_db.occupation == form.occupation.data
        assert participant_db.completed_form == True
        assert participant_db.completed_study == False
