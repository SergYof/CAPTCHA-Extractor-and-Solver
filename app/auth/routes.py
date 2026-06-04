from flask import Blueprint, request, render_template, flash
from werkzeug.security import generate_password_hash
from pathlib import Path
from app.models.user import User
from app.extensions import db
from app import ALLOWED_UPLOAD_EXTENSIONS

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    document = request.files.get("document")

    
    if not (username and password and document):
        flash("One or more of the fields are empty. Please fill in all the fields.", "error")
        return render_template("register.html")

    if not document.filename:
        flash("Please submit a file with a valid name", "error")
        return render_template("register.html")    

    extension = Path(document.filename).suffix.lower()
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        flash("Please only submit files with allowed extensions.", "error")
        return render_template("register.html")


    user = User(
        username=username,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.flush() # required in order to receive user ID

    filename = f"user{user.id}{extension}"
    document.save(filename)
    user.document_filename = filename
    
    db.session.commit()

    flash("Your account was created successfully! We'll take a look at your document, and you're good to go.", "ok")
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # TODO: login logic with Flask-Login
    return render_template("login.html")