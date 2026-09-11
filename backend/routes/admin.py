import logging

from flask import Blueprint, g, jsonify, request

from backend.extensions import db
from backend.models.item import Item
from backend.models.report import Report
from backend.models.user import User
from backend.services.admin_service import compute_statistics, update_report_status
from backend.utils.auth import roles_required

logger = logging.getLogger(__name__)

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/access-check")
@roles_required("ADMIN", "MODERATOR")
def access_check():
    return jsonify({"success": True, "data": {"authorized": True}, "message": "Administrative access granted."})


@admin_bp.get("/users")
@roles_required("ADMIN", "MODERATOR")
def users():
    records = db.session.scalars(db.select(User).order_by(User.created_at.desc())).all()
    return jsonify({"success": True, "data": {"users": [user.to_public_dict() for user in records]}, "message": "Users loaded."})


@admin_bp.get("/items")
@roles_required("ADMIN", "MODERATOR")
def items():
    records = db.session.scalars(db.select(Item).order_by(Item.created_at.desc())).all()
    return jsonify({"success": True, "data": {"items": [item.to_dict() for item in records]}, "message": "Items loaded."})


@admin_bp.get("/reports")
@roles_required("ADMIN", "MODERATOR")
def reports():
    records = db.session.scalars(db.select(Report).order_by(Report.created_at.desc())).all()
    return jsonify({"success": True, "data": {"reports": [report.to_dict() for report in records]}, "message": "Reports loaded."})


@admin_bp.put("/reports/<int:report_id>")
@roles_required("ADMIN", "MODERATOR")
def update_report(report_id):
    status = (request.get_json(silent=True) or {}).get("status", "")
    report, error = update_report_status(report_id, status)
    if error:
        code, message = error
        status_code = 404 if code == "REPORT_NOT_FOUND" else 400
        return jsonify({"success": False, "error": {"code": code, "message": message}}), status_code
    logger.info("Admin %s set report %s to %s", g.current_user.id, report_id, report.status)
    return jsonify({"success": True, "data": {"report": report.to_dict()}, "message": "Report status updated."})


@admin_bp.get("/statistics")
@roles_required("ADMIN", "MODERATOR")
def statistics():
    return jsonify({"success": True, "data": compute_statistics(), "message": "Statistics loaded."})
