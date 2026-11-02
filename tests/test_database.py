import os
import unittest
from datetime import date
from unittest.mock import patch

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.connection import create_database_engine, create_session_factory
from database.models import AuditLog, Base, GuestUsage, User
from database.security import decrypt_totp_secret, encrypt_totp_secret


class DatabaseFoundationTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_database_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session_factory = create_session_factory(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_authentication_tables_are_created(self):
        names = set(inspect(self.engine).get_table_names())
        self.assertTrue({"users", "oauth_accounts", "invitations", "sessions"}.issubset(names))
        self.assertTrue({"two_factor_methods", "recovery_codes", "guest_usage", "audit_logs"}.issubset(names))

    def test_user_defaults(self):
        with Session(self.engine) as session:
            user = User(email="danny@example.test", name="Danny")
            session.add(user)
            session.commit()
            session.refresh(user)
            self.assertEqual(user.role, "standard_user")
            self.assertFalse(user.email_verified)
            self.assertTrue(user.is_active)

    def test_database_rejects_invalid_user_role(self):
        with Session(self.engine) as session:
            session.add(User(email="invalid-role@example.test", role="superuser"))
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()

    def test_database_rejects_negative_guest_usage(self):
        with Session(self.engine) as session:
            session.add(GuestUsage(
                guest_key_hash="a" * 64,
                usage_date=date(2026, 1, 1),
                request_count=-1,
            ))
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()

    def test_audit_details_reject_sensitive_or_unknown_fields(self):
        with self.assertRaises(ValueError):
            AuditLog(event_type="login", outcome="failure", details={"password": "secret"})
        with self.assertRaises(ValueError):
            AuditLog(event_type="login", outcome="failure", details={"metadata": {"token": "secret"}})

    def test_audit_details_accept_allowlisted_metadata(self):
        log = AuditLog(
            event_type="oauth_login",
            outcome="success",
            details={"provider": "google", "reason_code": "verified"},
        )
        self.assertEqual(log.details, {"provider": "google", "reason_code": "verified"})

    def test_totp_secret_is_encrypted_and_requires_key(self):
        key = "MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA="
        with patch.dict(os.environ, {"PAI_AUTH_ENCRYPTION_KEY": key}):
            encrypted = encrypt_totp_secret("test-totp-secret")
            self.assertNotEqual(encrypted, "test-totp-secret")
            self.assertEqual(decrypt_totp_secret(encrypted), "test-totp-secret")
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                encrypt_totp_secret("test-totp-secret")

    def test_sqlite_foreign_keys_are_enabled(self):
        with self.engine.connect() as connection:
            result = connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one()
        self.assertEqual(result, 1)

    def test_non_sqlite_database_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SQLite only"):
            create_database_engine("postgresql://user:pass@localhost/db")


if __name__ == "__main__":
    unittest.main()
