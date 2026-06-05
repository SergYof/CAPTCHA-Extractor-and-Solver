from flask import Blueprint, render_template, flash, abort, send_from_directory, current_app, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import select, update
from pathlib import Path
from app.models import User
from app.extensions import db
from .scripts import admin_required, remove_user_document

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@admin_required
def dashboard():
    pending_requests = db.session.execute(
        select(User).where(User.status == "pending")
    ).scalars().all()
    
    return render_template("dashboard.html", current_user=current_user, requests=pending_requests)


@admin_bp.route("/admin/documents")
@admin_required
def view_document():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        abort(400, "Missing user_id in request")
    
    user = db.get_or_404(User, user_id)
    
    if not user.document_filename:
        return "File not found"
    
    return send_from_directory(
        Path(current_app.instance_path) / "uploads",
        user.document_filename,
    )


@admin_bp.route("/admin/approve", methods=["POST"])
@admin_required
def approve_request():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        abort(400, "Missing user_id in request")
    
    user = db.session.get(User, user_id)

    if user:
        user.status = "approved"
        db.session.commit()

        remove_user_document(user)

        flash(f"User {user.username} (ID {user_id}) approved.", "ok")
    else:
        flash(f"Error approving user {user_id}: user not found.", "error")
    
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/admin/reject", methods=["POST"])
@admin_required
def reject_request():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        abort(400, "Missing user_id in request")
    
    user = db.session.get(User, user_id)

    if user:
        user.status = "rejected"
        db.session.commit()

        remove_user_document(user)

        flash(f"User {user.username} (ID {user_id}) rejected.", "ok")
    else:
        flash(f"Error rejecting user {user_id}: user not found.", "error")
    
    return redirect(url_for("admin.dashboard"))