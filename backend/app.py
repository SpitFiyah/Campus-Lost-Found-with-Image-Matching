import logging
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import Config
from backend.extensions import db
from backend.routes.admin import admin_bp
from backend.routes.auth import auth_bp
from backend.routes.health import health_bp
from backend.routes.items import items_bp
from backend.routes.matches import matches_bp
from backend.routes.messages import messages_bp
from backend.routes.notifications import notifications_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"].split(","), supports_credentials=True)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(notifications_bp)

    @app.errorhandler(413)
    def request_entity_too_large(_error):
        return jsonify(
            {
                "success": False,
                "error": {"code": "FILE_TOO_LARGE", "message": "The uploaded file is too large."},
            }
        ), 413

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(
            {
                "success": False,
                "error": {"code": "NOT_FOUND", "message": "The requested resource was not found."},
            }
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Unhandled server error: %s", error)
        return jsonify(
            {
                "success": False,
                "error": {"code": "INTERNAL_ERROR", "message": "Something went wrong on our end. Please try again."},
            }
        ), 500

    logging.basicConfig(level=logging.INFO)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
