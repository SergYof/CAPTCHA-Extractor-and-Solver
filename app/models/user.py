from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    document_filename = db.Column(db.String(69))

    status = db.Column(
        db.String(20),
        default="pending"
    )


    def __init__(self, username, password_hash, document_filename=None):
        self.username = username
        self.password_hash = password_hash
        self.document_filename = document_filename