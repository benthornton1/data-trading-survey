from datetime import date
import mimetypes
import os
import random
import string

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from sqlalchemy import or_, and_
from werkzeug.datastructures import FileStorage, Headers
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.decorators import (
    admin_required,
    valid_admin_required,
    check_delete,
    check_edit,
)
from app.admin.forms import StudyForm, CardSetForm, UserGroupForm
from app.models import (
    Card,
    CardSet,
    DataValueLabel,
    HeatMap,
    Participant,
    Study,
    User,
    UserGroup,
)


@bp.route("")
@login_required
@admin_required
def index():
    studies = current_user.studies
    for study in studies:
        if study.name is None:
            studies.remove(study)
            db.session.delete(study)
            db.session.commit()

    card_sets = current_user.card_sets
    for card_set in card_sets:
        if card_set.name is None:
            card_sets.remove(card_set)
            db.session.delete(card_set)
            db.session.commit()

    user_groups = current_user.user_groups
    for user_group in user_groups:
        if user_group.name is None:
            user_groups.remove(user_group)
            db.session.delete(user_group)
            db.session.commit()

    return render_template(
        "admin/index.html",
        studies=studies,
        card_sets=card_sets,
        user_groups=user_groups,
    )


@bp.route("/study/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@valid_admin_required(model="study")
@check_edit
def study(id, study):
    form = StudyForm(
        data_values=study.data_values,
        number_of_columns=study.number_of_columns,
        number_of_rows=study.number_of_rows,
    )

    form.user_group.query = UserGroup.query.filter(
        UserGroup.creator == current_user
    ).filter(or_(UserGroup.study == study, UserGroup.study == None))

    form.card_set_x.query = CardSet.query.filter(
        CardSet.creator == current_user
    )

    form.card_set_y.query = CardSet.query.filter(
        CardSet.creator == current_user
    )

    if form.validate_on_submit():
        study.name = form.name.data
        study.description = form.desc.data


        if form.image.data is not None:
            file = form.image.data
            file_name = secure_filename(file.filename)
            file_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "img",
                "study_images",
                str(current_user.id),
                file_name,
            )

            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

            file.save(file_path)
            study.image = file_name

        study.card_set_x = form.card_set_x.data
        study.card_set_y = form.card_set_y.data

        study.data_values = form.data_values.data

        for label in study.data_value_labels:
            db.session.delete(label)
        db.session.commit()

        labels = []
        for label in form.data_value_labels.data:
            if label is not "":
                labels.append(DataValueLabel(label=label, study_id=study.id))

        study.data_value_labels = labels
        study.number_of_columns = form.number_of_columns.data
        study.number_of_rows = form.number_of_rows.data
        study.user_group = form.user_group.data
        study.start_date = form.start_date.data
        study.end_date = form.end_date.data

        try:
            db.session.commit()
            flash("Study Created/ Updated Succesfully")
            return redirect(url_for("admin.index"))
        except Exception as error:
            flash("There was a problem creating your study")
            db.session.rollback()

    elif request.method == "GET":

        form.name.data = study.name
        form.desc.data = study.description
        form.card_set_x.data = study.card_set_x
        form.card_set_y.data = study.card_set_y
        for idx, label in enumerate(study.data_value_labels):
            form_label = form.data_value_labels[idx]
            form_label.data = label.label
        form.start_date.data = study.start_date
        form.end_date.data = study.end_date

        if form.name.data is not None:
            form.submit.label.text = "Update"

    return render_template("admin/study.html", form=form, study=study)


@bp.route("/card_set/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@valid_admin_required(model="card_set")
@check_edit
def card_set(id, card_set):
    form = CardSetForm()

    if form.validate_on_submit():

        old_cards = Card.query.filter(Card.card_set == card_set).delete()
        for study in card_set.studies_x:
            old_heat_maps = HeatMap.query.filter(study=study).delete()
        for study in card_set.studies_y:
            old_heat_maps = HeatMap.query.filter(study=study).delete()
        db.session.commit()

        card_set.name = form.card_set_name.data
        card_set.measure = form.measure.data

        card_list = []

        for card in form.cards.data:

            file = card.get("image")
            if file is not None:
                file_name = secure_filename(file.filename)
                file_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    "img",
                    "card_images",
                    str(current_user.id),
                    file_name,
                )
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                card_list.append(
                    Card(
                        name=card.get("card_name"),
                        description=card.get("desc"),
                        image=file_name,
                        creator=current_user,
                    )
                )
            else:

                card_list.append(
                    Card(
                        name=card.get("card_name"),
                        description=card.get("desc"),
                        creator=current_user,
                    )
                )

        card_set.cards = card_list

        try:
            db.session.commit()
            flash("Card Set Created/ Updated Succesfully.")
            return redirect(url_for("admin.index"))
        except:
            flash("There was an error adding your Card Set")
            db.session.rollback()

    elif request.method == "GET":
        form.card_set_name.data = card_set.name
        form.measure.data = card_set.measure

        for card in card_set.cards:
            form.cards.append_entry(
                dict(
                    card_name=card.name,
                    desc="" if card.description is None else card.description,
                    image="" if card.image is None else card.image,
                )
            )
    return render_template("admin/card_set.html", form=form)


@bp.route("/user_group/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@valid_admin_required(model="user_group")
@check_edit
def user_group(id, user_group):
    form = UserGroupForm()
    study = Study.query.filter_by(user_group_id=user_group.id).first()
    if form.validate_on_submit():
        # replace attributes upon re-sumbission of form with updates, preventing duplicate users.

        user_group.name = form.name.data

        # delete all old participants
        Participant.query.filter_by(user_group=user_group).delete()
        db.session.commit()

        for user in form.users.data:
            # Create new User object for all emails in the form
            username = "".join(
                random.choice(string.ascii_letters) for i in range(8)
            )
            while (
                Participant.query.filter_by(username=username).first() != None
            ):
                username = "".join(
                    random.choice(string.ascii_letters) for i in range(8)
                )
            new_participant = Participant(
                email=user.get("email"), username=username
            )
            user_group.users.append(new_participant)

        try:
            db.session.commit()
            flash("User Group Created/ Updated Succesfully.")
            return redirect(url_for("admin.index"))
        except Exception as error:
            flash("There was a problem updating your User Group")
            db.session.rollback()
    elif request.method == "GET":
        form.name.data = user_group.name
        for user in user_group.users:
            form.users.append_entry({"email": user.email})
        if form.name.data is not None:
            form.submit.label.text = "Update"

    return render_template("admin/user_group.html", form=form)


@bp.route("/new_study")
@login_required
@admin_required
def new_study():
    try:
        study = Study()
        study.creator = current_user
        db.session.add(study)
        db.session.commit()
        return redirect(url_for("admin.study", id=study.id))
    except Exception as error:
        flash("There was a problem creating a new Study.")
        return redirect(url_for("admin.index"))


@bp.route("/new_user_group")
@login_required
@admin_required
def new_user_group():
    try:
        user_group = UserGroup()
        user_group.creator = current_user
        db.session.add(user_group)
        db.session.commit()
        return redirect(url_for("admin.user_group", id=user_group.id))
    except Exception as error:
        flash("There was a problem creating a new User Group.")
        return redirect(url_for("admin.index"))


@bp.route("/new_card_set")
@login_required
@admin_required
def new_card_set():
    try:
        card_set = CardSet()
        card_set.creator = current_user
        db.session.add(card_set)
        db.session.commit()

        return redirect(url_for("admin.card_set", id=card_set.id))
    except Exception as error:
        db.session.rollback()
        flash("There was a problem creating a new Card Set.")
        return redirect(url_for("admin.index"))


@bp.route("/delete/study/<int:id>", methods=["POST", "GET"])
@login_required
@admin_required
@valid_admin_required(model="study")
@check_delete
def delete_study(id, study):
    try:
        db.session.delete(study)
        db.session.commit()
        flash("Study {} succesfully deleted.".format(study.name))
        return redirect(url_for("admin.index"))
    except Exception as error:
        db.session.rollback()
        flash("There was a problem deleting this Study.")
        return redirect(url_for("admin.index"))


@bp.route("/delete/user_group/<int:id>", methods=["POST", "GET"])
@login_required
@admin_required
@valid_admin_required(model="user_group")
@check_delete
def delete_user_group(id, user_group):
    try:
        db.session.delete(user_group)
        db.session.commit()
        flash("User Group {} succesfully deleted.".format(user_group.name))
        return redirect(url_for("admin.index"))
    except Exception as error:
        db.session.rollback()
        flash("There was a problem deleting this User Group.")
        return redirect(url_for("admin.index"))


@bp.route("/delete/card_set/<int:id>", methods=["POST", "GET"])
@login_required
@admin_required
@valid_admin_required(model="card_set")
@check_delete
def delete_card_set(id, card_set):
    try:
        db.session.delete(card_set)
        db.session.commit()
        flash("Card Set {} succesfully deleted.".format(card_set.name))
        return redirect(url_for("admin.index"))
    except Exception as error:
        db.session.rollback()
        flash("There was a problem deleting this Card Set.")
        return redirect(url_for("admin.index"))
