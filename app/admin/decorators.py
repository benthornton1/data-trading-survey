from flask_login import current_user
from flask import redirect, url_for
from functools import wraps

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return wrapper
