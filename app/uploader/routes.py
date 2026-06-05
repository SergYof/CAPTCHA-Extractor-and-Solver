from flask import Blueprint, request, jsonify
from app.scripts import cors_enabled, processPicture


uploader_bp = Blueprint("uploader", __name__)


@uploader_bp.route("/submit_picture", methods=["GET"])
@cors_enabled
def submit_picture():
    """
    Used to submit the picture extracted by the injected script.
    Returns the numbers (indices) of tiles to check.
    """
    
    return jsonify(processPicture(request.args))