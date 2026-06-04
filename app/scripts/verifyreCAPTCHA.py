import requests
from app import VERIFY_URL, RECAPTCHA_SECRET_KEY


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