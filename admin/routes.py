from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_dashboard():
    return render_template("dashboard.html", current_user=None) # TODO