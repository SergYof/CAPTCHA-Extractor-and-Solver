from app.extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    document_filename = db.Column(db.String(64))

    status = db.Column(
        db.String(20),
        default="pending"
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(self, username, password_hash, document_filename=None):
        self.username = username
        self.password_hash = password_hash
        self.document_filename = document_filename