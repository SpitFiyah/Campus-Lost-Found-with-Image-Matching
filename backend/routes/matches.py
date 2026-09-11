from flask import Blueprint, g, jsonify

from backend.extensions import db
from backend.models.item import Item
from backend.models.match import Match
from backend.services.notification_service import create_notification
from backend.utils.auth import login_required

matches_bp = Blueprint("matches", __name__, url_prefix="/api/matches")


def failure(code, message, status):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status


def owned_match(match):
    return match and (match.lost_item.user_id == g.current_user.id or match.found_item.user_id == g.current_user.id)


@matches_bp.get("")
@login_required
def my_matches():
    own_item_ids = db.session.scalars(db.select(Item.id).where(Item.user_id == g.current_user.id)).all()
    matches = db.session.scalars(
        db.select(Match)
        .where(Match.lost_item_id.in_(own_item_ids) | Match.found_item_id.in_(own_item_ids))
        .order_by(Match.final_score.desc())
    ).all()
    return jsonify({"success": True, "data": {"matches": [match.to_dict() for match in matches]}, "message": "Your matches loaded."})


@matches_bp.get("/item/<int:item_id>")
@login_required
def item_matches(item_id):
    item = db.session.get(Item, item_id)
    if not item or item.user_id != g.current_user.id:
        return failure("FORBIDDEN", "You can only view matches for your own reports.", 403)
    matches = db.session.scalars(db.select(Match).where((Match.lost_item_id == item_id) | (Match.found_item_id == item_id)).order_by(Match.final_score.desc())).all()
    return jsonify({"success": True, "data": {"matches": [match.to_dict() for match in matches]}, "message": "Potential matches loaded."})


@matches_bp.post("/<int:match_id>/<action>")
@login_required
def update_match(match_id, action):
    match = db.session.get(Match, match_id)
    if not owned_match(match):
        return failure("MATCH_NOT_FOUND", "Match not found.", 404)
    if action not in ("accept", "reject"):
        return failure("INVALID_ACTION", "Action must be accept or reject.", 400)
    match.status = "ACCEPTED" if action == "accept" else "REJECTED"
    if action == "accept":
        match.lost_item.status = "MATCHED"
        match.found_item.status = "MATCHED"
    other_user_id = match.found_item.user_id if g.current_user.id == match.lost_item.user_id else match.lost_item.user_id
    create_notification(other_user_id, f"Match {match.status.lower()}", f"A potential match for {match.lost_item.name} was {match.status.lower()}.", f"MATCH_{match.status}", match.lost_item_id, match.id)
    db.session.commit()
    return jsonify({"success": True, "data": {"match": match.to_dict()}, "message": f"Match {match.status.lower()}."})


@matches_bp.post("/<int:match_id>/returned")
@login_required
def returned(match_id):
    match = db.session.get(Match, match_id)
    if not owned_match(match):
        return failure("MATCH_NOT_FOUND", "Match not found.", 404)
    match.lost_item.status = "RETURNED"
    match.found_item.status = "RETURNED"
    create_notification(match.lost_item.user_id, "Item returned", f"{match.lost_item.name} was marked returned.", "ITEM_RETURNED", match.lost_item_id, match.id)
    db.session.commit()
    return jsonify({"success": True, "data": {"match": match.to_dict()}, "message": "Item marked returned."})
