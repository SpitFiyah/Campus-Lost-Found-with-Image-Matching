from flask import Blueprint, jsonify


health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.get("/health")
def health_check():
    return jsonify(
        {
            "success": True,
            "data": {"service": "campus-lost-found-api", "status": "ok"},
            "message": "API is running",
        }
    )
