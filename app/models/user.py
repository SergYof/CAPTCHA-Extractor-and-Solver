from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(256))

    status = db.Column(
        db.String(20),
        default="pending"
    )