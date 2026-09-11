# Development Log

## 2026-09-11

### Implemented

- Hardened the backend: embedding caching on `ItemImage.embedding_path`,
  error handling around the matching pipeline instead of unhandled 500s,
  structured logging for auth failures/matching failures/admin actions,
  a `GET /api/items/locations` endpoint, a `GET /api/matches` aggregate
  endpoint, and item update/report-flagging logic moved into the service
  layer so routes stay thin.
- Rebuilt the entire frontend on a single dependency-free design system
  (`frontend/css/app.css`, `frontend/js/{util,layout}.js`) — dropped
  Bootstrap, fixed the matches page showing the wrong side of a match to
  the viewer, rendered item photos for the first time anywhere in the
  app, and closed a stored-XSS gap where item/message/notification text
  was interpolated into `innerHTML` unescaped.
- Completed features that existed on the backend with no frontend path:
  messaging compose/reply, profile editing, admin flagged-report review,
  match "mark as returned," and multi-image upload.
- Corrected documentation and UI copy that overclaimed "AI" (the
  matching service is a color-histogram similarity score, not a
  pretrained model) and removed a self-authored "beautification
  complete" changelog file.

### Decisions

- Kept the frontend framework-free (no bundler, no JS framework) and
  added only a minimal shared header/util module — enough to stop
  duplicating nav markup across ~20 pages without introducing a build
  step this project doesn't need.
- Left the color-histogram embedding as-is rather than swapping in a
  pretrained model: it has no GPU/model-download dependency, is fully
  explainable, and the project's own standards call for documenting
  limitations over overclaiming capability.

### Issues

- MySQL is still the documented production database; local
  verification of this pass ran against SQLite (`tests/` already did;
  manual API verification used a throwaway `sqlite:///dev.sqlite3`).
  MySQL-specific schema behavior (enums, `ON UPDATE CURRENT_TIMESTAMP`)
  was not re-verified against a live MySQL instance in this pass.

### Next

- Add IDOR/authorization tests for matches, messages, and notification
  ownership; unit tests for `scoring.py`/`similarity.py`; and route
  tests for the previously-untested `messages.py`/`notifications.py`/
  `admin.py` surface.
- Grow the matching evaluation beyond the synthetic same/unrelated-color
  fixture test as real report photos accumulate.
