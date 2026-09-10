from functools import wraps

from flask import g, jsonify, session

from backend.extensions import db
from backend.models.user import User


def load_current_user():
    user_id = session.get("user_id")
    g.current_user = db.session.get(User, user_id) if user_id else None
    if user_id and g.current_user is None:
        session.clear()
    return g.current_user


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if load_current_user() is None:
            return jsonify(
                {
                    "success": False,
                    "error": {"code": "AUTHENTICATION_REQUIRED", "message": "Sign in to continue."},
                }
            ), 401
        return view(*args, **kwargs)

    return wrapped_view


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):
            if g.current_user.role not in roles:
                return jsonify(
                    {
                        "success": False,
                        "error": {"code": "FORBIDDEN", "message": "You do not have permission for this action."},
                    }
                ), 403
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
