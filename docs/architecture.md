# Architecture

Campus Lost & Found is a modular monolith. The browser uses the Fetch API to call Flask REST blueprints. Routes validate HTTP concerns and delegate business rules to services. SQLAlchemy models represent the MySQL contract, while image processing is isolated behind an image matching engine so the embedding model can be replaced later.

```text
frontend (static HTML, plain JavaScript, no framework)
              |
        Flask REST API
              |
 authentication | items | matching | messaging | admin services
              |
       SQLAlchemy + MySQL
              |
     file storage + embeddings
```

The frontend is deliberately dependency-free: no build step, no Bootstrap, no
JS framework. `frontend/css/app.css` is the single component library (buttons,
cards, forms, badges, tables, empty/error/loading states). `frontend/js/api.js`
is the one `fetch` wrapper every page uses; `frontend/js/util.js` holds
`escapeHtml()` and small render/format helpers; `frontend/js/layout.js` renders
the shared header/nav into a `<header id="site-header">` placeholder each page
includes, so the nav isn't hand-duplicated across ~20 static HTML files.

Session cookies carry authentication (`SESSION_COOKIE_SAMESITE` is `Lax` by
default, which works because the frontend and API share `localhost` in
development; see `.env.example` for the note on deploying frontend and API to
different hostnames, which requires `SameSite=None` and HTTPS).

Development phases 1-7 from the original project brief are all implemented:
foundation, auth, item reporting with image upload, embeddings/matching/
notifications, messaging and the return workflow, admin moderation and
analytics, and this UI/security/documentation pass.
