from datetime import date
from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from app.models import Card, CardSet, HeatMap, Response, Study, User, UserGroup


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.type == "admin":
            return function(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return wrapper


def valid_admin_required(model):
    def decorator(function):
        @wraps(function)
        def wrapper2(id):
            if model == "card_set":
                card_set = CardSet.query.filter_by(id=id).first_or_404()
                if card_set.creator_id == current_user.id:
                    return function(id, card_set=card_set)
                else:
                    return redirect(url_for("auth.login"))
            elif model == "study":
                study = Study.query.filter_by(id=id).first_or_404()
                if study.creator_id == current_user.id:
                    return function(id, study=study)
                else:
                    return redirect(url_for("auth.login"))
            elif model == "user_group":
                user_group = UserGroup.query.filter_by(id=id).first_or_404()
                if user_group.creator_id == current_user.id:
                    return function(id, user_group=user_group)
                else:
                    return redirect(url_for("auth.login"))
            else:
                return redirect("auth.login")

        return wrapper2

    return decorator


def check_study_date(studies):
    for study in studies:
        if study.start_date:
            if study.start_date <= date.today():
                return False
    return True


def check_delete(function):
    @wraps(function)
    def wrapper3(*args, **kwargs):
        if "user_group" in kwargs:
            user_group = kwargs["user_group"]
            if user_group.study:
                string = "You cannot delete this User Group as it is currently associated with {study} Study, remove this association before deleting this User Group.".format(
                    study=user_group.study
                )
                flash(string)
                return redirect(url_for("admin.index"))
            else:
                return function(*args, **kwargs)
        if "card_set" in kwargs:
            card_set = kwargs["card_set"]
            if card_set.studies_x:
                studies_str = str(
                    [study.name for study in card_set.studies_x]
                )[1:-1]
                string = "You cannot delete this Card Set as it is currently associated with {studies} Studies, remove these associations before deleting this Card Set.".format(
                    studies=studies_str
                )
                flash(string)
                return redirect(url_for("admin.index"))
            if card_set.studies_y:
                studies_str = str(
                    [study.name for study in card_set.studies_y]
                )[1:-1]
                string = "You cannot delete this Card Set as it is currently associated with {studies} Studies, remove these associations before deleting this Card Set.".format(
                    studies=studies_str
                )
                flash(string)
                return redirect(url_for("admin.index"))
            else:
                return function(*args, **kwargs)
        if "study" in kwargs:
            study = kwargs["study"]
            if not check_study_date([study]):
                flash(
                    "You cannot delete this Study as it is currently in progress."
                )
                return redirect(url_for("admin.index"))
            else:
                return function(*args, **kwargs)
        return function(*args, **kwargs)

    return wrapper3


def check_edit(function):
    @wraps(function)
    def wrapper4(*args, **kwargs):
        if "user_group" in kwargs:
            user_group = kwargs["user_group"]
            if user_group.study:
                if not check_study_date([user_group.study]):
                    flash(
                        "You cannot edit this User Group as the Study associated with it is currently in progress."
                    )
                    return redirect(url_for("admin.index"))
                else:
                    return function(*args, **kwargs)
        if "card_set" in kwargs:
            card_set = kwargs["card_set"]
            if card_set.studies_x:
                if not check_study_date(card_set.studies_x):
                    flash(
                        "You cannot edit this Card Set as there are Studies associated with it which are currently in progress."
                    )
                    return redirect(url_for("admin.index"))
                else:
                    return function(*args, **kwargs)
            elif card_set.studies_y:
                if not check_study_date(card_set.studies_y):
                    flash(
                        "You cannot edit this Card Set as there are Studies associated with it which are currently in progress."
                    )
                    return redirect(url_for("admin.index"))
                else:
                    return function(*args, **kwargs)
        if "study" in kwargs:
            study = kwargs["study"]
            if not check_study_date([study]):
                flash(
                    "You cannot edit this Study as it is currently in progress."
                )
                return redirect(url_for("admin.index"))
            else:
                return function(*args, **kwargs)
        return function(*args, **kwargs)

    return wrapper4
