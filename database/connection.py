"""SQLite engine and session factory helpers.

The database is created lazily so importing the existing AI application does
not create files or change its startup behaviour.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_DB_PATH = ".personal_ai_os/auth.sqlite3"


def database_url() -> str:
    """Return the configured SQLite URL."""
    raw_path = os.getenv("PAI_DB_PATH", DEFAULT_DB_PATH)
    if raw_path == ":memory:":
        return "sqlite+pysqlite:///:memory:"
    path = Path(raw_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+pysqlite:///{path.resolve().as_posix()}"


def create_database_engine(url: str | None = None) -> Engine:
    """Create a SQLite engine with foreign-key enforcement enabled."""
    resolved_url = url or database_url()
    kwargs: dict[str, object] = {"pool_pre_ping": True}
    if resolved_url.endswith(":memory:"):
        from sqlalchemy.pool import StaticPool

        kwargs.update(
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_engine(resolved_url, **kwargs)

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection: object, _record: object) -> None:
        cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Return a session factory bound to the supplied engine."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session(factory: sessionmaker[Session]) -> Iterator[Session]:
    """Yield a session and always close it."""
    session = factory()
    try:
        yield session
    finally:
        session.close()
