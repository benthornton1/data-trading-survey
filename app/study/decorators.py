from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from app.models import Study


def valid_participant_required(function):
    @wraps(function)
    def wrapper3(*args, **kwargs):
        study = Study.query.filter_by(id=kwargs["id"]).first_or_404()
        if current_user.user_group == study.user_group:
            kwargs["study"] = study
            return function(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return wrapper3


def check_complete_study(function):
    @wraps(function)
    def wrapper4(*args, **kwargs):
        if current_user.completed_study == False:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("study.complete"))

    return wrapper4


def check_not_completed_study(function):
    @wraps(function)
    def wrapper5(*args, **kwargs):
        if current_user.completed_study == True:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return wrapper5


def participant_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.type == "participant":
            return function(*args, **kwargs)
        else:

            return redirect(url_for("auth.login"))

    return wrapper


def completed_info_form_required(function):
    @wraps(function)
    def wrapper2(*args, **kwargs):
        if current_user.completed_form == True:
            return function(*args, **kwargs)
        else:
            flash("You must complete this form before accessing that.")
            return redirect(url_for("study.user_info"))

    return wrapper2
