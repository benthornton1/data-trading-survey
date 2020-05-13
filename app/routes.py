from flask import redirect, url_for

from app import bp


@bp.route("")
def index():
    return redirect(url_for("auth.login"))


@bp.route("/tests")
def tests():
    return render_template("tests.html")
