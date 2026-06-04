from flask import Blueprint, request
from app.scripts import cors_enabled, processPicture


uploader_bp = Blueprint("uploader", __name__)


@uploader_bp.route("/submit_picture", methods=["GET"])
@cors_enabled
def submit_picture():
    """
    Used to submit the picture extracted by the injected script.
    Returns the numbers (indices) of tiles to check.
    """

    picURL = request.args.get("picURL", None)   # get the picture URL supplied by the GET request
    if not picURL:
        return "No picture URL provided!"
    
    result = processPicture(picURL)
    return result if result else "No response :("