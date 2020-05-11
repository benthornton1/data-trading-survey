from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User, Admin, Participant


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        try:
            if current_user.type == "admin":
                return redirect(url_for("admin.index"))
            else:
                return redirect(url_for("study.user_info"))
        except:
            return redirect(url_for("auth.login"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        if user.type == "participant" and user.completed_study is True:
            flash("You have already completed this study.")
            return redirect(url_for("auth.login"))
        login_user(user)
        if user.type == "admin":
            return redirect(url_for("admin.index"))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("study.user_info")
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
