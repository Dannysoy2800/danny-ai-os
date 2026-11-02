"""Alembic migration safety and lifecycle tests."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text

from database.connection import create_database_engine
from database.init_db import initialize_database
from database.models import Base


class DatabaseMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "auth.sqlite3")
        self.env = patch.dict(os.environ, {"PAI_DB_PATH": self.db_path})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp_dir.cleanup()

    def _config(self):
        config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
        return config

    def test_fresh_database_upgrades_to_head_and_keeps_audit_triggers(self):
        initialize_database()
        engine = create_database_engine()
        try:
            inspector = inspect(engine)
            names = set(inspector.get_table_names())
            self.assertTrue({
                "users", "oauth_accounts", "invitations", "sessions",
                "two_factor_methods", "recovery_codes",
                "email_verification_tokens", "password_reset_tokens",
                "guest_usage", "audit_logs", "alembic_version",
            }.issubset(names))
            triggers = {
                row[0] for row in engine.connect().execute(text(
                    "SELECT name FROM sqlite_master WHERE type='trigger'"
                ))
            }
            self.assertIn("trg_audit_details_validate_insert", triggers)
            self.assertIn("trg_audit_details_validate_update", triggers)
            with engine.connect() as connection:
                self.assertEqual(connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one(), 1)
        finally:
            engine.dispose()

    def test_upgrade_is_idempotent(self):
        initialize_database()
        initialize_database()
        engine = create_database_engine()
        try:
            with engine.connect() as connection:
                version = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            self.assertEqual(version, "0001_auth_schema")
        finally:
            engine.dispose()

    def test_unversioned_existing_schema_is_rejected_without_modification(self):
        engine = create_database_engine()
        try:
            Base.metadata.create_all(engine)
        finally:
            engine.dispose()

        with self.assertRaisesRegex(RuntimeError, "no Alembic version"):
            initialize_database()

        engine = create_database_engine()
        try:
            self.assertNotIn("alembic_version", inspect(engine).get_table_names())
            self.assertIn("users", inspect(engine).get_table_names())
        finally:
            engine.dispose()

    def test_downgrade_removes_initial_schema(self):
        initialize_database()
        command.downgrade(self._config(), "base")
        engine = create_database_engine()
        try:
            self.assertEqual(inspect(engine).get_table_names(), [])
        finally:
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
