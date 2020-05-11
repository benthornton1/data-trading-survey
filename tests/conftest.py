import shutil
import os

import pytest

from app import create_app, db
from app.models import (
    Admin,
    Card,
    CardSet,
    DataValueLabel,
    Participant,
    Study,
    User,
    UserGroup,
)
from datetime import date, timedelta
from flask_login import login_user


@pytest.fixture(scope="module")
def client():
    os.environ["FLASK_ENV"] = "test"
    flask_app = create_app()

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()
    # with flask_app.app_context():
    yield testing_client

    fp = os.path.join(flask_app.config["UPLOAD_FOLDER"], "pdf")
    try:
        shutil.rmtree(fp)
    except Exception as e:
        print(e)

    ctx.pop()


@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
