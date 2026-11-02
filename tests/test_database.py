import unittest

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from database.connection import create_database_engine, create_session_factory
from database.models import Base, User


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

    def test_user_defaults_and_role_constraint(self):
        with Session(self.engine) as session:
            user = User(email="danny@example.test", name="Danny")
            session.add(user)
            session.commit()
            session.refresh(user)
            self.assertEqual(user.role, "standard_user")
            self.assertFalse(user.email_verified)
            self.assertTrue(user.is_active)

    def test_sqlite_foreign_keys_are_enabled(self):
        with self.engine.connect() as connection:
            result = connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one()
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
