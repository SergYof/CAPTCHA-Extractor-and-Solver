from flask import Blueprint, request, render_template
from app.models.user import User
from app.extensions import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    user = User(
        username=request.form.get("username")
    )
    db.session.add(user)
    db.session.commit()

    return render_template("register.html")
    return "OK"


@auth_bp.route("/login")
def login():
    return render_template("login.html")