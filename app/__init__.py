from dotenv import load_dotenv
import os
from flask import Flask


load_dotenv()


VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")

ALLOWED_UPLOAD_EXTENSIONS = (".pdf", ".jpg", ".png")


from app.auth import auth_bp
from app.admin import admin_bp
from app.testing import testing_bp
from app.uploader import uploader_bp
from app.extensions import db, login_manager


blueprints = (
    auth_bp,
    admin_bp,
    testing_bp,
    uploader_bp,
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.instance_path}\\app.db"
    print(app.config["SQLALCHEMY_DATABASE_URI"]) # TODO: remove
    db.init_app(app)
    login_manager.init_app(app)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    return app


app = create_app()
