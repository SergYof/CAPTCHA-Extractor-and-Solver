import os
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from sqlalchemy import select
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

    upload_folder = os.path.join(current_app.instance_path, "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"user_{user.id}{extension}"
    document.save(os.path.join(upload_folder, filename))

    user.document_filename = filename
    
    db.session.commit()

    flash("Your account was created successfully! We'll take a look at your document, and you're good to go.", "ok")
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        flash("One or more of the fields are empty.", "Error")
        return render_template("login.html")
    
    user = db.session.scalar(
        select(User).where(User.username == username)
    )

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        flash("Successfully loggged in!", "ok")
        return redirect(url_for("testing.captcha_form"))
    else:
        flash("Non-existent user or incorrect password.", "error")
        return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))