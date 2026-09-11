# Campus Lost & Found

A campus-focused lost and found platform that combines report metadata with intelligent image similarity to identify potential matches. Image matching supports discovery; it does not confirm ownership.

## Current status

The full report -> match -> message -> return workflow is implemented end to
end: authentication and profiles, lost/found reporting with multi-image
upload, automatic image-similarity matching with notifications, in-platform
messaging, match accept/reject/return actions, and an admin console (users,
all reports, flagged-report review, and statistics). See
`docs/architecture.md` for how the pieces fit together and
`docs/matching-algorithm.md` for exactly how matching works (a color-histogram
similarity score, not a pretrained model) and its known limitations.

## Run on Windows

Prerequisites: Python 3.11+ and MySQL 8+.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.txt
Copy-Item .env.example .env
```

Create the database and tables with `mysql -u root -p < database/schema.sql`, then update `DATABASE_URL` in `.env` with a least-privilege MySQL account. Start the API from the repository root:

```powershell
py -m backend.app
```

Or launch both servers together:

```powershell
.\start.ps1
```

Command Prompt users can run `start.bat`. The launcher expects `.venv` and `.env` to exist, serves the frontend at `http://localhost:5500`, and runs Flask at `http://localhost:5000`.

The API is available at `http://localhost:5000/api/health`. The landing page is available at `http://localhost:5500`.

To load demonstration users, images, a lost/found pair, a potential match, and notifications:

```powershell
.\.venv\Scripts\python.exe -m database.seed
```

Demo accounts use the password `demoPass123` and the college emails `asha@campus.edu` and `noah@campus.edu`. Neither demo account is an admin; promote one via SQL (`UPDATE users SET role = 'ADMIN' WHERE college_email = '...'`) to reach `/admin/*`.

Running without MySQL installed (e.g. to try the frontend locally): set `DATABASE_URL=sqlite:///dev.sqlite3` in `.env` instead. `tests/` already runs entirely against an in-memory SQLite database and needs no database server at all.

## Project structure

```text
backend/      app factory, config, extensions, routes, models, services, matching, utils, uploads
frontend/     public and student HTML pages, admin pages, css, js
database/     schema.sql, seed.py
docs/         architecture, database, API, matching decisions, development log
tests/        pytest suite (auth, items, matching, and more)
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```
