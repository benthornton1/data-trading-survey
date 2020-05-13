from datetime import date
import itertools

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.wrappers import Response as WrkResponse
from munch import munchify

from app import db
from app.models import CardSet, Response, Study, HeatMap, CardPosition, DataValue, DataValueLabel, Response2, Card
from app.study import bp
from app.study.decorators import *
from app.study.forms import UserInfoForm
import pdb

@bp.route("/index")
@bp.route("/")
@login_required
@participant_required
@completed_info_form_required
@check_complete_study
def index():
    return render_template(
        "study/index.html", study=current_user.user_group.study
    )


@bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
@participant_required
@valid_participant_required
@completed_info_form_required
@check_complete_study
def study(id, study):

    if request.method == "POST":
        data = request.get_json()
        dv = []
        cp = []
        cards_x_munch = munchify(data.get('cards_x'))
        cards_y_munch = munchify(data.get('cards_y'))   
        data_values_munch = munchify(data.get('data_values'))
        
        for col, cards in cards_x_munch.items():
            
            col_num = int(col.split('_')[1])
            for card in cards:
                card_db = Card.query.filter_by(id=card.id).first()
                card_position = CardPosition(position=col_num, card=card_db)
                db.session.add(card_position)
                cp.append(card_position)

        for row, cards in cards_y_munch.items():
            
            row_num = int(row.split('_')[1])
            for card in cards:
                card_db = Card.query.filter_by(id=card.id).first()
                card_position = CardPosition(position=row_num, card=card_db)
                db.session.add(card_position)
                cp.append(card_position)
                
        for col_row, data_values in data_values_munch.items():
            col_num = int(col_row.split('_')[1])
            row_num = int(col_row.split('_')[3])
            
            for data_value in data_values:
                data_value_label = DataValueLabel.query.filter_by(id=data_value.id).first()
                if data_value.value is not None:
                    data_value = DataValue(column=col_num, row=row_num, value=data_value.value, data_value_label=data_value_label) 
                    db.session.add(data_value)
                    dv.append(data_value)
                

        response2 = Response2(study=study, participant=current_user, card_positions=cp, data_values=dv)
        pdb.set_trace()
        db.session.add(response2)
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
            flash(
                "There was a problem submitting your information. Please try again."
            )
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
            flash(
                "There was a problem submitting your information. Please try again."
            )
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
