"""
Declarative base for SQLAlchemy models.

Kept separate from session.py to avoid circular imports once Alembic
migrations are added in the next phase.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
