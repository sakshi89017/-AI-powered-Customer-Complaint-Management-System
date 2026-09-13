"""
Database session and engine management.

Connects to PostgreSQL using DATABASE_URL defined in application settings.
Provides dependency injection generator `get_db()` and table initialisation `init_db()`.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base

logger = logging.getLogger(__name__)
settings = get_settings()

# Configure engine arguments based on dialect
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency for yielding database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialise database tables defined in SQLAlchemy models."""
    try:
        # Import models so Base has metadata registered
        import app.models.complaint  # noqa: F401

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as exc:
        logger.error("Failed to initialize database tables: %s", exc)
        # We log the error but don't prevent the app from starting up
