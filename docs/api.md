# API Conventions

All endpoints return one of these shapes:

```json
{"success": true, "data": {}, "message": "..."}
```

```json
{"success": false, "error": {"code": "CODE", "message": "..."}}
```

Authentication uses an HTTP-only Flask session cookie (`SESSION_COOKIE_SAMESITE`
and `SESSION_COOKIE_SECURE` are configurable via `.env`; see
`docs/architecture.md` for the cross-host caveat). Endpoints marked "auth"
require a signed-in session and return `401 AUTHENTICATION_REQUIRED` otherwise.
Endpoints marked "admin" additionally require the `ADMIN` or `MODERATOR` role
and return `403 FORBIDDEN` otherwise.

## Health

- `GET /api/health`

## Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session` — `{authenticated, user}`, `user` is `null` when signed out.
- `GET /api/auth/me` (auth)
- `GET /api/auth/profile` (auth)
- `PUT /api/auth/profile` (auth) — updates `name`, `department`, `phone`.

## Items

- `GET /api/items` — filters: `q`, `type`, `category`, `color`, `location`, `status`, `date`, `user_id`.
- `GET /api/items/locations` — the canonical campus location list used by the report form.
- `POST /api/items` (auth) — `multipart/form-data`, one or more files under `images`.
- `GET /api/items/<id>`
- `PUT /api/items/<id>` (auth, owner only) — editable fields: `name`, `category`, `description`, `color`, `location`.
- `DELETE /api/items/<id>` (auth, owner only) — soft-closes the report (`status = CLOSED`).
- `GET /api/items/<id>/matches` (auth, owner only) — delegates to `GET /api/matches/item/<id>`.
- `POST /api/items/<id>/report` (auth) — flags the report for admin review.
- `GET /api/items/images/<filename>` — serves an uploaded image.

## Matches

- `GET /api/matches` (auth) — every match across the current user's own reports.
- `GET /api/matches/item/<item_id>` (auth, owner only) — matches for one report.
- `POST /api/matches/<id>/accept` (auth, either side of the match)
- `POST /api/matches/<id>/reject` (auth, either side of the match)
- `POST /api/matches/<id>/returned` (auth, either side of the match)

## Messages

- `GET /api/messages` (auth) — every message sent or received by the current user.
- `POST /api/messages` (auth) — `receiver_id`, `message`, optional `item_id`. If
  `item_id` is set, the sender must either own that item or be messaging its
  owner.

## Notifications

- `GET /api/notifications` (auth) — includes `unread_count`.
- `PUT /api/notifications/<id>/read` (auth, owner only)

## Admin

- `GET /api/admin/access-check` (admin)
- `GET /api/admin/users` (admin)
- `GET /api/admin/items` (admin) — every report, including other users' reports.
- `GET /api/admin/reports` (admin) — the flagged-report queue.
- `PUT /api/admin/reports/<id>` (admin) — `status` one of `PENDING`, `REVIEWED`, `DISMISSED`, `ACTIONED`.
- `GET /api/admin/statistics` (admin) — totals, return rate, and `hotspots`/`categories` breakdowns.
