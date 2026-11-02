"""Explicit database initialization command."""
from __future__ import annotations

from database.connection import create_database_engine
from database.models import Base


def initialize_database() -> None:
    """Create all currently declared tables.

    For production schema evolution, use versioned Alembic migrations rather
    than relying on create_all to alter existing tables.
    """
    engine = create_database_engine()
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    initialize_database()
    print("Danny AI OS database initialized.")
