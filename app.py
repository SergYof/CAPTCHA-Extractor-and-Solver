from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
from dotenv import load_dotenv
from processPicture import processPicture


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")

VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def verify_recaptcha(token: str, remoteip: str | None = None) -> tuple[bool, dict]:
    """
    Verify reCAPTCHA token with Google.
    Returns: (success, full_response_json)
    """
    data = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": token,
    }
    if remoteip:
        data["remoteip"] = remoteip

    r = requests.post(VERIFY_URL, data=data, timeout=10)
    r.raise_for_status()
    result = r.json()
    return bool(result.get("success")), result


@app.route("/", methods=["GET"])
def index():
    if not RECAPTCHA_SITE_KEY or not RECAPTCHA_SECRET_KEY:
        flash("חסרים מפתחות reCAPTCHA. בדוק את קובץ .env", "error")
    return render_template("index.html", site_key=RECAPTCHA_SITE_KEY)


@app.route("/submit", methods=["POST"])
def submit():
    token = request.form.get("g-recaptcha-response", "")
    if not token:
        flash("נא להשלים CAPTCHA.", "error")
        return redirect(url_for("index"))

    try:
        ok, result = verify_recaptcha(token, remoteip=request.remote_addr)
    except requests.RequestException as e:
        flash(f"שגיאת תקשורת מול Google: {e}", "error")
        return redirect(url_for("index"))

    if not ok:
        # תוכל להדפיס/ללוג את result כדי לראות error-codes
        flash(f"CAPTCHA נכשל. קוד: {result.get('error-codes')}", "error")
        return redirect(url_for("index"))

    return render_template("success.html", result=result)


@app.route("/submit_picture", methods=["GET"])
def submit_picture():
    """
    Used to submit the picture extracted by the injected script.
    Returns the numbers (indices) of tiles to check.
    """

    picURL = request.args.get("picURL", None)   # get the URL supplied by the GET request
    if not picURL:
        return "No picture URL provided!"
    
    return processPicture(picURL)


if __name__ == "__main__":
    # TODO: the browser will complain that the certificate is invalid, better replace it with a real one
    app.run(debug=True, ssl_context=("certs/localhost+2.pem", "certs/localhost+2-key.pem")) 
