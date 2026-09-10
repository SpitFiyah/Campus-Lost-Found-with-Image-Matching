# Campus Lost & Found

A campus-focused lost and found platform that combines report metadata with intelligent image similarity to identify potential matches. Image matching supports discovery; it does not confirm ownership.

## Current status

Phase 1 foundation and Phase 2 authentication are implemented. The app includes Flask app factory, MySQL configuration, SQLAlchemy extension, CORS policy, upload limits, consistent JSON errors, secure session authentication, role-aware authorization, profile updates, frontend auth forms, and a normalized schema contract.

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

The API is available at `http://localhost:5000/api/health`. The Phase 1 landing page is available at `http://localhost:5500`.

To load demonstration users, images, a lost/found pair, a potential match, and notifications:

```powershell
.\.venv\Scripts\python.exe -m database.seed
```

Demo accounts use the password `demoPass123` and the college emails `asha@campus.edu` and `noah@campus.edu`.

## Planned structure

```text
backend/      app factory, config, extensions, routes, models, services, matching, utils, uploads
frontend/     public and student HTML pages, admin pages, css, js
database/     schema.sql, seed.sql
docs/         architecture, database, API, matching decisions
```

## Development phases

1. Foundation and database contract (complete)
2. Authentication, roles, and student profiles (complete)
3. Item reporting, secure image uploads, and search
4. Embeddings, candidate retrieval, weighted matching, and notifications
5. Messaging, ownership verification, and return workflow
6. Admin moderation, analytics, hotspots, seed data, and full tests
7. UI refinement, security review, documentation, and demonstration readiness

Before Phase 3, verify registration/login from the browser, the health endpoint, MySQL schema import, frontend-to-API CORS requests, and clean installation from a fresh virtual environment.
