from flask import url_for, render_template
from flask_login import current_user 
from werkzeug.exceptions import HTTPException

from app.errors import bp

@bp.app_errorhandler(HTTPException)
def handle_not_found(e):
    try:
        if current_user.type == 'admin':
            return render_template('error.html', error_code=e.code, error_name=e.name, url=url_for('admin.index')), e.code
        if current_user.type == 'participant':
            return render_template('error.html', error_code=e.code, error_name=e.name, url=url_for('study.index')), e.code
    except AttributeError:
        return render_template('error.html', error_code=e.code, error_name=e.name, url=url_for('auth.login')), e.code