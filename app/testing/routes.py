import requests
from flask import Blueprint, render_template, flash, request, redirect, url_for
from app import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from app.scripts import verify_recaptcha


testing_bp = Blueprint("testing", __name__)


@testing_bp.route("/", methods=["GET"])
def captcha_form():
    if not RECAPTCHA_SITE_KEY or not RECAPTCHA_SECRET_KEY:
        flash("reCAPTCHA keys not found. Please check the .env file.", "error")
    return render_template("index.html", site_key=RECAPTCHA_SITE_KEY)


@testing_bp.route("/submit", methods=["POST"])
def submit():
    token = request.form.get("g-recaptcha-response", "")
    if not token:
        flash("Please complete CAPTCHA.", "error")
        return redirect(url_for("index"))

    try:
        ok, result = verify_recaptcha(token, remoteip=request.remote_addr)
    except requests.RequestException as e:
        flash(f"Communication error with Google: {e}.", "error")
        return redirect(url_for("index"))

    if not ok:
        flash(f"CAPTCHA failed. Code: {result.get('error-codes')}", "error")
        return redirect(url_for("index"))

    return render_template("success.html", result=result)