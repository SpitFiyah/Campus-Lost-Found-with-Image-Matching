from flask import Blueprint, jsonify, request

from sqlalchemy import func
from backend.extensions import db
from backend.models.item import Item
from backend.models.match import Match
from backend.models.report import Report
from backend.models.user import User
from backend.utils.auth import roles_required


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
    report = db.session.get(Report, report_id)
    status = str((request.get_json(silent=True) or {}).get("status", "")).upper()
    if not report:
        return jsonify({"success": False, "error": {"code": "REPORT_NOT_FOUND", "message": "Report not found."}}), 404
    if status not in {"PENDING", "REVIEWED", "DISMISSED", "ACTIONED"}:
        return jsonify({"success": False, "error": {"code": "INVALID_STATUS", "message": "Invalid report status."}}), 400
    report.status = status
    db.session.commit()
    return jsonify({"success": True, "data": {"report": report.to_dict()}, "message": "Report status updated."})


@admin_bp.get("/statistics")
@roles_required("ADMIN", "MODERATOR")
def statistics():
    total_items = db.session.scalar(db.select(func.count(Item.id))) or 0
    lost = db.session.scalar(db.select(func.count(Item.id)).where(Item.type == "LOST")) or 0
    found = db.session.scalar(db.select(func.count(Item.id)).where(Item.type == "FOUND")) or 0
    returned = db.session.scalar(db.select(func.count(Item.id)).where(Item.status == "RETURNED")) or 0
    pending = db.session.scalar(db.select(func.count(Match.id)).where(Match.status == "PENDING")) or 0
    by_location = db.session.execute(db.select(Item.location, func.count(Item.id)).group_by(Item.location).order_by(func.count(Item.id).desc())).all()
    return jsonify({"success": True, "data": {"total_users": db.session.scalar(db.select(func.count(User.id))) or 0, "total_items": total_items, "lost_reports": lost, "found_reports": found, "returned_items": returned, "pending_matches": pending, "return_rate": round(returned / total_items * 100, 2) if total_items else 0, "hotspots": [{"location": location, "reports": count} for location, count in by_location]}, "message": "Statistics loaded."})
