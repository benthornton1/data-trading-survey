from datetime import date, timedelta

from flask import url_for

from app.admin.forms import StudyForm
from app.models import CardSet, HeatMap, Response, Study, UserGroup
from tests.helpers import (
    create_admin,
    create_card_set,
    create_study,
    create_user_group,
    login,
)


def test_create_valid_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin, user group and 2 card sets 
    WHEN '/admin/new_study/1 is requested (GET)
    WHEN '/admin/study/1' is posted with valid data (POST)
    THEN check response is valid and study has been created.
    """
    with client.application.test_request_context():
        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        card_set_x = create_card_set(client, creator=admin)
        card_set_y = create_card_set(client, creator=admin)
        user_group = create_user_group(client, creator=admin)
        response = client.get(
            url_for("admin.new_study"), follow_redirects=True
        )

        form = StudyForm()
        assert bytes(form.name.label.text, "utf-8") in response.data
        assert bytes(form.desc.label.text, "utf-8") in response.data
        assert bytes(form.image.label.text, "utf-8") in response.data
        assert bytes(form.card_set_x.label.text, "utf-8") in response.data
        assert bytes(form.card_set_y.label.text, "utf-8") in response.data
        assert bytes(form.data_values.label.text, "utf-8") in response.data
        assert (
            bytes(form.number_of_columns.label.text, "utf-8") in response.data
        )
        assert bytes(form.number_of_rows.label.text, "utf-8") in response.data
        assert bytes(form.user_group.label.text, "utf-8") in response.data
        assert bytes(form.start_date.label.text, "utf-8") in response.data
        assert bytes(form.start_date.label.text, "utf-8") in response.data
        assert bytes(form.end_date.label.text, "utf-8") in response.data
        assert bytes(form.submit.label.text, "utf-8") in response.data

        form.name.data = "Test Study"
        form.card_set_x.data = card_set_x.id
        form.card_set_y.data = card_set_y.id
        form.data_values.data = 0
        form.number_of_columns.data = 2
        form.number_of_rows.data = 2
        form.user_group.data = user_group.id
        form.start_date.data = date.today()
        form.end_date.data = date.today() + timedelta(days=3)
        form.submit.data = True
        response = client.post(
            url_for("admin.study", id=1), data=form.data, follow_redirects=True
        )

        study_db = Study.query.filter_by(id=1).first()

        assert response.status_code == 200
        assert b"Study Created/ Updated Succesfully" in response.data
        assert bytes(study_db.name, "utf-8") in response.data
        assert bytes(study_db.card_set_x.name, "utf-8") in response.data
        assert bytes(study_db.card_set_y.name, "utf-8") in response.data
        assert bytes(study_db.user_group.name, "utf-8") in response.data
        assert bytes(str(study_db.start_date), "utf-8") in response.data
        assert bytes(str(study_db.end_date), "utf-8") in response.data
        assert bytes(study_db.description, "utf-8") in response.data
        if not study_db.image:
            assert bytes("no_image.jpg", "utf-8")
        else:
            assert bytes(str(study_db.image), "utf-8") in response.data
        assert bytes(str(study_db.data_values), "utf-8") in response.data
        assert bytes(str(study_db.number_of_columns), "utf-8") in response.data
        assert bytes(str(study_db.number_of_rows), "utf-8") in response.data
        assert bytes("No", "utf-8") in response.data
        assert len(study_db.heat_maps) == (
            len(study_db.card_set_x.cards)
            * len(study_db.card_set_y.cards)
            * len(study_db.data_value_labels)
        ) + (len(study_db.card_set_x.cards) * len(study_db.card_set_y.cards))


def test_create_invalid_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin, user group and 2 card sets 
    WHEN '/admin/new_study/1 is requested (GET)
    WHEN '/admin/study/1' is posted with invalid data (POST)
    THEN check response is valid and study has not been created.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        card_set_x = create_card_set(client, creator=admin)
        card_set_y = create_card_set(client, creator=admin)
        user_group = create_user_group(client, creator=admin)

        response = client.get(
            url_for("admin.new_study"), follow_redirects=True
        )

        form = StudyForm()

        form.name.data = None
        form.card_set_x.data = card_set_x.id
        form.card_set_y.data = card_set_x.id
        form.data_values.data = 4
        form.number_of_columns.data = 0
        form.number_of_rows.data = 0
        form.user_group.data = 5
        form.start_date.data = date.today() - timedelta(days=3)
        form.end_date.data = date.today() - timedelta(days=4)
        form.submit.data = True

        response = client.post(
            url_for("admin.study", id=1), data=form.data, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Not a valid choice" in response.data
        assert b"This field is required" in response.data
        assert b"The start date cannot be in the past." in response.data
        assert (
            b"The end date cannot be before the start date." in response.data
        )
        assert b"The end date cannot be in the past." in response.data
        assert (
            b"Card Set for x-axis cannot have the same value as Card Set for y-axis."
            in response.data
        )


def test_delete_current_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin, a current study
    WHEN '/admin/delete_study/1' is requested (GET)
    THEN check response is valid and study has not been deleted.
    """

    with client.application.test_request_context():
        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        study = create_study(client, creator=admin)
        response = client.get(
            url_for("admin.delete_study", id=study.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert (
            b"You cannot delete this Study as it is currently in progress."
            in response.data
        )

        study_db = Study.query.filter_by(id=study.id).first()

        assert study_db is not None
        assert study_db.name == study.name
        assert study_db.description == study.description
        assert study_db.image == study.image
        assert study_db.data_values == study.data_values
        assert study_db.number_of_columns == study.number_of_columns
        assert study_db.number_of_rows == study.number_of_rows
        assert study_db.start_date == study.start_date
        assert study_db.end_date == study.end_date
        assert study_db.card_set_x == study.card_set_x
        assert study_db.card_set_y == study.card_set_y
        assert study_db.data_value_labels == study.data_value_labels
        assert study_db.heat_maps == study.heat_maps
        assert study_db.responses == study.responses
        assert study_db.user_group == study.user_group


def test_delete_future_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin, a future study
    WHEN '/admin/delete_study/1' is requested (GET)
    THEN check response is valid and study has been deleted.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        study = create_study(
            client,
            name="Test Study",
            creator=admin,
            start_date=date.today() + timedelta(days=1),
        )

        response = client.get(
            url_for("admin.delete_study", id=study.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Study Test Study succesfully deleted" in response.data

        assert Study.query.filter_by(id=1).first() is None
        assert UserGroup.query.filter_by(id=1).first() is None
        assert CardSet.query.filter_by(id=1).first() is not None
        assert HeatMap.query.all() == []
        assert Response.query.all() == []


def test_edit_current_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a current study. 
    WHEN '/admin/study/1' is requested (GET).
    THEN check response is valid and user is redirected and cannot edit the study.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        study = create_study(client, creator=admin, start_date=date.today())
        response = client.get(
            url_for("admin.study", id=study.id), follow_redirects=True
        )

        assert response.status_code == 200
        assert (
            b"You cannot edit this Study as it is currently in progress."
            in response.data
        )


def test_edit_future_study(client, init_database):
    """
    GIVEN a Flask application, logged in admin and a current study. 
    WHEN '/admin/study/1' is requested (GET).
    THEN check response is valid and user is not redirected and can edit the study.
    """
    with client.application.test_request_context():
        admin = create_admin(client, username="admin", password="password")
        login(client, username="admin", password="password")

        study = create_study(
            client, start_date=date.today() + timedelta(days=3), creator=admin
        )
        response = client.get(
            url_for("admin.study", id=1), follow_redirects=True
        )

        assert response.status_code == 200
        # assert urlparse(response.location).path == url_for('admin.index')
        assert b"Test Study" in response.data

        form = StudyForm()
        form.name.data = "Test Updated Study"
        form.card_set_x.data = study.card_set_x.id
        form.card_set_y.data = study.card_set_y.id
        form.data_values.data = 0
        form.number_of_columns.data = 3
        form.number_of_rows.data = 3
        form.user_group.data = study.user_group.id
        form.start_date.data = date.today() + timedelta(days=2)
        form.end_date.data = date.today() + timedelta(days=5)
        form.submit.data = True

        response = client.post(
            url_for("admin.study", id=study.id),
            data=form.data,
            follow_redirects=True,
        )

        assert response.status_code == 200

        updated_study = Study.query.filter_by(id=study.id).first()

        assert updated_study is not None
        assert updated_study.name == form.name.data
        assert updated_study.number_of_columns == form.number_of_columns.data
        assert updated_study.number_of_rows == form.number_of_rows.data
        assert updated_study.start_date == form.start_date.data
        assert updated_study.end_date == form.end_date.data
        assert len(updated_study.heat_maps) == (
            len(study.card_set_x.cards)
            * len(study.card_set_y.cards)
            * len(study.data_value_labels)
        ) + (len(study.card_set_x.cards) * len(study.card_set_y.cards))
        assert len(updated_study.data_value_labels) == len(
            study.data_value_labels
        )
