from pathlib import Path

from flask import Blueprint, current_app, g, jsonify, request, send_from_directory

from backend.services.item_service import create_item, search_items
from backend.utils.auth import login_required


items_bp = Blueprint("items", __name__, url_prefix="/api/items")


def error_response(code, message, status):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status


@items_bp.get("")
def list_items():
    items, error = search_items(request.args)
    if error:
        return error_response(error[0], error[1], 400)
    return jsonify({"success": True, "data": {"items": [item.to_dict() for item in items]}, "message": "Items loaded."})


@items_bp.post("")
@login_required
def create():
    item, error = create_item(g.current_user.id, request.form, request.files.getlist("images"), current_app.config["UPLOAD_FOLDER"])
    if error:
        return error_response(error[0], error[1], 400)
    from backend.services.matching_service import process_item_matches

    process_item_matches(item, current_app.config["UPLOAD_FOLDER"])
    return jsonify({"success": True, "data": {"item": item.to_dict(include_private=True)}, "message": "Item reported successfully."}), 201


@items_bp.get("/<int:item_id>")
def detail(item_id):
    from backend.extensions import db
    from backend.models.item import Item

    item = db.session.get(Item, item_id)
    if not item or item.status == "REMOVED":
        return error_response("ITEM_NOT_FOUND", "Item report not found.", 404)
    return jsonify({"success": True, "data": {"item": item.to_dict()}, "message": "Item loaded."})


@items_bp.get("/<int:item_id>/matches")
@login_required
def item_matches(item_id):
    from backend.routes.matches import item_matches as matches_for_item
    return matches_for_item(item_id)


@items_bp.put("/<int:item_id>")
@login_required
def update(item_id):
    from backend.extensions import db
    from backend.models.item import Item
    item = db.session.get(Item, item_id)
    if not item or item.status == "REMOVED":
        return error_response("ITEM_NOT_FOUND", "Item report not found.", 404)
    if item.user_id != g.current_user.id:
        return error_response("FORBIDDEN", "You can only edit your own reports.", 403)
    for field in ("name", "category", "description", "color", "location"):
        if field in request.form and request.form[field].strip():
            setattr(item, field, request.form[field].strip())
    db.session.commit()
    return jsonify({"success": True, "data": {"item": item.to_dict(include_private=True)}, "message": "Item updated successfully."})


@items_bp.delete("/<int:item_id>")
@login_required
def delete(item_id):
    from backend.extensions import db
    from backend.models.item import Item
    item = db.session.get(Item, item_id)
    if not item or item.user_id != g.current_user.id:
        return error_response("ITEM_NOT_FOUND", "Item report not found.", 404)
    item.status = "CLOSED"
    db.session.commit()
    return jsonify({"success": True, "data": {}, "message": "Item report closed."})


@items_bp.post("/<int:item_id>/report")
@login_required
def report_item(item_id):
    from backend.extensions import db
    from backend.models.item import Item
    from backend.models.report import Report

    item = db.session.get(Item, item_id)
    data = request.get_json(silent=True) or {}
    reason = str(data.get("reason", "")).strip()
    if not item or item.status == "REMOVED":
        return error_response("ITEM_NOT_FOUND", "Item report not found.", 404)
    if not reason or len(reason) > 80:
        return error_response("INVALID_REPORT", "A report reason is required.", 400)
    report = Report(reporter_id=g.current_user.id, item_id=item.id, reason=reason, description=str(data.get("description", "")).strip()[:500] or None)
    db.session.add(report)
    db.session.commit()
    return jsonify({"success": True, "data": {"report": report.to_dict()}, "message": "Report submitted for review."}), 201


@items_bp.get("/images/<path:filename>")
def image(filename):
    safe_filename = Path(filename).name
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], safe_filename)
