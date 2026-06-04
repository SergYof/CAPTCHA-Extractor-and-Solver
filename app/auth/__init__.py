from .routes import auth_bp
from app.extensions import login_manager, db
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))