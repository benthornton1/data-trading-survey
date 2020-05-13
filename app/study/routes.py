from datetime import date
import itertools

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.wrappers import Response as WrkResponse
from munch import munchify

from app import db
from app.models import (
    CardSet,
    Response,
    Study,
    CardPosition,
    DataValue,
    DataValueLabel,
    Response,
    Card,
)
from app.study import bp
from app.study.decorators import *
from app.study.forms import UserInfoForm
from app.study.helpers import convert_response


@bp.route("/index")
@bp.route("/")
@login_required
@participant_required
@completed_info_form_required
@check_complete_study
def index():
    return render_template("study/index.html", study=current_user.user_group.study)


@bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
@participant_required
@valid_participant_required
@completed_info_form_required
@check_complete_study
def study(id, study):

    if request.method == "POST":
        data = request.get_json()

        cards_x = data.get("cards_x")
        cards_y = data.get("cards_y")
        data_values = data.get("data_values")

        response = convert_response(cards_x, cards_y, data_values)
        response.study = study
        response.participant = current_user

        db.session.add(response)
        current_user.completed_study = True
        db.session.commit()

        return dict(url=url_for("study.complete"))

    return render_template(
        "study/study.html",
        study=study,
        card_set_x=study.card_set_x,
        card_set_y=study.card_set_y,
        creator_id=study.creator_id,
    )


@bp.route("/user_info", methods=["POST", "GET"])
@login_required
@participant_required
@check_complete_study
def user_info():
    form = UserInfoForm()
    if form.validate_on_submit():
        current_user.gender = form.gender.data
        current_user.age_group = form.age_group.data
        current_user.country_of_birth = form.nationality.data
        current_user.education_level = form.education_level.data
        current_user.occupation = form.occupation.data
        current_user.latest_country = form.latest_country.data
        current_user.income = form.income.data
        current_user.completed_form = True
        try:
            db.session.commit()
            return redirect(url_for("study.index"))
        except:
            flash("There was a problem submitting your information. Please try again.")
            db.session.rollback()
    if request.method == "GET":
        form.gender.data = current_user.gender
        form.age_group.data = current_user.age_group
        form.nationality.data = current_user.country_of_birth
        form.education_level.data = current_user.education_level
        form.occupation.data = current_user.occupation
        form.latest_country.data = current_user.latest_country
        form.income.data = current_user.income
    return render_template("study/user_info.html", form=form)


@bp.route("/change_info", methods=["POST", "GET"])
@login_required
@participant_required
@completed_info_form_required
@check_complete_study
def change_info():
    form = UserInfoForm()

    if form.validate_on_submit():
        current_user.gender = form.gender.data
        current_user.age_group = form.age_group.data
        current_user.country_of_birth = form.nationality.data
        current_user.education_level = form.education_level.data
        current_user.occupation = form.occupation.data
        current_user.latest_country = form.latest_country.data
        current_user.income = form.income.data
        current_user.completed_form = True
        try:
            db.session.commit()
            return redirect(url_for("study.index"))
        except:
            flash("There was a problem submitting your information. Please try again.")
            db.session.rollback()
    if request.method == "GET":
        form.gender.data = current_user.gender
        form.age_group.data = current_user.age_group
        form.nationality.data = current_user.country_of_birth
        form.education_level.data = current_user.education_level
        form.occupation.data = current_user.occupation
        form.latest_country.data = current_user.latest_country
        form.income.data = current_user.income

    return render_template("study/change_user_info.html", form=form)


@bp.route("/complete")
@login_required
@participant_required
@completed_info_form_required
@check_not_completed_study
def complete():
    return render_template("study/complete.html")
