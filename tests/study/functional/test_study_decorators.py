from urllib.parse import urlparse

from flask import url_for
from flask_login import current_user

from app import db
from tests.helpers import (
    create_admin,
    create_participant,
    create_study,
    create_user_group,
    login,
)


def test_valid_participant_required_invalid(client, init_database):
    """
    GIVEN a Flask application, participant not in study
    WHEN routes with @valid_participant_required is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        participant = create_participant(client, username="p", password="p")
        study = create_study(client)
        login(client, username="p", password="p")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        client.get(url_for("auth.logout"))


def test_valid_participant_required_valid(client, init_database):
    """
    GIVEN a Flask application, participant in study
    WHEN routes with @valid_participant_required is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(
            client,
            username="participant",
            password="password",
            completed_form=True,
        )
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)
        login(client, username="participant", password="password")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )

        assert bytes(study.card_set_x.cards[0].name, "utf-8") in response.data
        client.get(url_for("auth.logout"))


def test_check_complete_study(client, init_database):
    """
    GIVEN a Flask application, participant in study
    WHEN routes with @valid_participant_required is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(
            client, username="p", password="p", completed_form=True
        )
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        login(client, username="p", password="p")
        participant.completed_study = True
        db.session.commit()

        response = client.get(
            url_for("study.index", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")
        response = client.get(
            url_for("study.user_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")
        response = client.get(
            url_for("study.change_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.complete")

        client.get(url_for("auth.logout"))


def test_participant_required(client, init_database):
    """
    GIVEN a Flask application, participant in study
    WHEN routes with @participant_required is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        admin = create_admin(client, username="admin2", password="password")
        participant = create_participant(client, completed_form=True)
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        # with admin
        login(client, username="admin2", password="password")
        response = client.get(
            url_for("study.index", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.user_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.change_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.complete", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        client.get(url_for("auth.logout"))

        # with anon
        response = client.get(
            url_for("study.index", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.user_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.change_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        response = client.get(
            url_for("study.complete", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")
        client.get(url_for("auth.logout"))


def test_complete_info_form_required(client, init_database):
    """
    GIVEN a Flask application, participant in study, incompleted info form
    WHEN routes with @completed_info_form_required is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        participant = create_participant(
            client, username="p", password="p", completed_form=False
        )
        admin = create_admin(client, username="a", password="p")
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        login(client, username="p", password="p")

        response = client.get(
            url_for("study.index", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.user_info")
        response = client.get(
            url_for("study.study", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.user_info")
        response = client.get(
            url_for("study.change_info", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.user_info")
        response = client.get(
            url_for("study.complete", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("study.user_info")


def test_check_not_completed_study(client, init_database):
    """
    GIVEN a Flask application, participant in study, incomplete study & compelete study.
    WHEN routes with @check_not_completed_study is requested (GET)
    THEN check redirect location
    """
    with client.application.test_request_context():
        participant = create_participant(
            client, username="p", password="p", completed_form=True
        )
        admin = create_admin(client, username="a", password="p")
        user_group = create_user_group(
            client, creator=admin, participants=[participant]
        )
        study = create_study(client, creator=admin, user_group=user_group)

        login(client, username="p", password="p")

        response = client.get(
            url_for("study.complete", id=study.id), follow_redirects=False
        )
        assert urlparse(response.location).path == url_for("auth.login")

        participant.completed_study = True
        db.session.commit()

        response = client.get(
            url_for("study.complete", id=study.id), follow_redirects=False
        )
        assert b"<h3>Thank You!</h3>" in response.data
        assert (
            b"<p>Thanks for participating in the study, you can now log out of the system.</p>"
            in response.data
        )
