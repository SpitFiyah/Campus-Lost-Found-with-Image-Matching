import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://campus_user:campus_password@localhost/campus_lost_found",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))
    # Anchored to PROJECT_ROOT (not left as a bare relative path) so it
    # resolves the same way regardless of the server process's actual
    # working directory at launch time - a relative UPLOAD_FOLDER previously
    # meant uploaded files could be saved under one resolved path and later
    # requested under another, producing spurious 404s on image URLs.
    UPLOAD_FOLDER = str((PROJECT_ROOT / os.getenv("UPLOAD_FOLDER", "backend/uploads")).resolve())
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5500")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    UPLOAD_FOLDER = tempfile.mkdtemp(prefix="campus-lost-found-tests-")
