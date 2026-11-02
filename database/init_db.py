"""Explicit, versioned database initialization command."""
from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from database.connection import database_url, create_database_engine


def _alembic_config(url: str) -> Config:
    """Build an Alembic config using the same database URL as the app."""
    config_path = Path(__file__).resolve().parent.parent / "alembic.ini"
    config = Config(str(config_path))
    # ConfigParser treats '%' as interpolation syntax.
    config.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    return config


def initialize_database() -> None:
    """Upgrade a fresh or already-versioned database to the latest revision.

    Existing non-empty databases without an Alembic version are deliberately
    rejected. They require a separately reviewed backup/schema-adoption
    procedure; silently stamping or recreating them could hide schema drift
    or destroy existing data.
    """
    url = database_url()
    engine = create_database_engine(url)
    try:
        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())
        has_version_table = "alembic_version" in existing_tables
        db_path = os.getenv("PAI_DB_PATH", ".personal_ai_os/auth.sqlite3")
        is_memory = db_path == ":memory:"
        db_file = Path(db_path).expanduser() if not is_memory else None
        has_existing_file_data = bool(
            db_file is not None and db_file.exists() and db_file.stat().st_size > 0
        )

        application_tables = existing_tables - {"alembic_version"}
        if application_tables and not has_version_table:
            raise RuntimeError(
                "This database contains tables but has no Alembic version. "
                "No changes were made. Back up the database and complete a "
                "reviewed schema-adoption procedure before migrating it."
            )
        if has_existing_file_data and not existing_tables and not is_memory:
            # A non-empty SQLite file with no schema may be unrelated/corrupt.
            raise RuntimeError(
                "The configured SQLite file is non-empty but has no tables. "
                "No changes were made; inspect and back up the file first."
            )
    finally:
        engine.dispose()

    command.upgrade(_alembic_config(url), "head")


if __name__ == "__main__":
    initialize_database()
    print("Danny AI OS database is up to date.")
