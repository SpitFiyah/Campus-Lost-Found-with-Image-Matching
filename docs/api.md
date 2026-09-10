# API Conventions

All endpoints return one of these shapes:

```json
{"success": true, "data": {}, "message": "..."}
```

```json
{"success": false, "error": {"code": "CODE", "message": "..."}}
```

Implemented endpoints include `GET /api/health`, `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/session`, `GET /api/auth/me`, `GET /api/auth/profile`, `PUT /api/auth/profile`, and `GET /api/admin/access-check`.

Authentication uses an HTTP-only Flask session cookie. The admin access check accepts `ADMIN` and `MODERATOR` users and rejects students on the backend. Planned blueprints are items, matches, notifications, messages, and the remaining admin operations.

Item workflow endpoints include `GET /api/items`, `POST /api/items`, `GET /api/items/<id>`, `PUT /api/items/<id>`, `DELETE /api/items/<id>`, `GET /api/items/<id>/matches`, and `POST /api/items/<id>/report`. Match actions are available at `POST /api/matches/<id>/accept`, `POST /api/matches/<id>/reject`, and `POST /api/matches/<id>/returned`.
