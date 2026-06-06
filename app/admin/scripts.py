from flask import abort, current_app
from flask_login import current_user, login_required
from functools import wraps
from pathlib import Path


def admin_required(func):
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        
        return func(*args, *kwargs)

    return wrapper


def remove_user_document(user):
    # remove a document uploaded by user if it exists
    if user.document_filename:
        filepath = Path(current_app.instance_path) / "uploads" / user.document_filename

        if filepath.exists():
            filepath.unlink()
