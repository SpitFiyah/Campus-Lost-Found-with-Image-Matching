from sqlalchemy import func

from backend.extensions import db
from backend.models.item import Item
from backend.models.match import Match
from backend.models.report import Report
from backend.models.user import User


ALLOWED_REPORT_STATUSES = {"PENDING", "REVIEWED", "DISMISSED", "ACTIONED"}


def update_report_status(report_id, status):
    report = db.session.get(Report, report_id)
    if not report:
        return None, ("REPORT_NOT_FOUND", "Report not found.")
    status = str(status).upper()
    if status not in ALLOWED_REPORT_STATUSES:
        return None, ("INVALID_STATUS", "Invalid report status.")
    report.status = status
    db.session.commit()
    return report, None


def compute_statistics():
    total_items = db.session.scalar(db.select(func.count(Item.id))) or 0
    lost = db.session.scalar(db.select(func.count(Item.id)).where(Item.type == "LOST")) or 0
    found = db.session.scalar(db.select(func.count(Item.id)).where(Item.type == "FOUND")) or 0
    returned = db.session.scalar(db.select(func.count(Item.id)).where(Item.status == "RETURNED")) or 0
    pending_matches = db.session.scalar(db.select(func.count(Match.id)).where(Match.status == "PENDING")) or 0
    total_users = db.session.scalar(db.select(func.count(User.id))) or 0
    by_location = db.session.execute(
        db.select(Item.location, func.count(Item.id)).group_by(Item.location).order_by(func.count(Item.id).desc())
    ).all()
    by_category = db.session.execute(
        db.select(Item.category, func.count(Item.id)).group_by(Item.category).order_by(func.count(Item.id).desc())
    ).all()
    return {
        "total_users": total_users,
        "total_items": total_items,
        "lost_reports": lost,
        "found_reports": found,
        "returned_items": returned,
        "pending_matches": pending_matches,
        "return_rate": round(returned / total_items * 100, 2) if total_items else 0,
        "hotspots": [{"location": location, "reports": count} for location, count in by_location],
        "categories": [{"category": category, "reports": count} for category, count in by_category],
    }
