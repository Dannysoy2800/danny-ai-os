"""Create the initial authentication schema."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_auth_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320, collation="NOCASE"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("role IN ('admin', 'standard_user', 'guest')", name="ck_users_role"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "oauth_accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(length=30), nullable=False),
        sa.Column("provider_user_id", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("provider", "provider_user_id", name="uq_oauth_provider_subject"),
    )
    op.create_index("ix_oauth_accounts_user_id", "oauth_accounts", ["user_id"])
    op.create_table(
        "invitations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("invited_email", sa.String(length=320, collation="NOCASE"), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_invitations_email_status", "invitations", ["invited_email", "used_at", "revoked_at"])
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_user_expiry", "sessions", ["user_id", "expires_at"])
    op.create_table(
        "two_factor_methods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("encrypted_secret", sa.String(length=512), nullable=True),
        sa.Column("enabled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "recovery_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_recovery_codes_user_id", "recovery_codes", ["user_id"])
    op.create_table(
        "email_verification_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_email_verification_tokens_user_id", "email_verification_tokens", ["user_id"])
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"])
    op.create_table(
        "guest_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("guest_key_hash", sa.String(length=64), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=False),
        sa.Column("request_count", sa.Integer(), nullable=False),
        sa.UniqueConstraint("guest_key_hash", "usage_date", name="uq_guest_usage_day"),
        sa.CheckConstraint("request_count >= 0", name="ck_guest_usage_request_count_nonnegative"),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("outcome", sa.String(length=30), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_user_created", "audit_logs", ["user_id", "created_at"])
    op.execute("""
    CREATE TRIGGER trg_audit_details_validate_insert
    BEFORE INSERT ON audit_logs
    WHEN NEW.details IS NOT NULL
    BEGIN
      SELECT CASE WHEN json_valid(NEW.details) = 0 OR json_type(NEW.details) != 'object'
        THEN RAISE(ABORT, 'audit details must be a JSON object') END;
      SELECT CASE WHEN EXISTS (
        SELECT 1 FROM json_each(NEW.details)
        WHERE key NOT IN ('provider','reason_code','method','role','resource_type','resource_id','status_code')
          OR type NOT IN ('null','true','false','integer','text')
          OR (type = 'text' AND length(value) > 120)
      ) THEN RAISE(ABORT, 'audit details contain disallowed data') END;
    END;
    """)
    op.execute("""
    CREATE TRIGGER trg_audit_details_validate_update
    BEFORE UPDATE OF details ON audit_logs
    WHEN NEW.details IS NOT NULL
    BEGIN
      SELECT CASE WHEN json_valid(NEW.details) = 0 OR json_type(NEW.details) != 'object'
        THEN RAISE(ABORT, 'audit details must be a JSON object') END;
      SELECT CASE WHEN EXISTS (
        SELECT 1 FROM json_each(NEW.details)
        WHERE key NOT IN ('provider','reason_code','method','role','resource_type','resource_id','status_code')
          OR type NOT IN ('null','true','false','integer','text')
          OR (type = 'text' AND length(value) > 120)
      ) THEN RAISE(ABORT, 'audit details contain disallowed data') END;
    END;
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_audit_details_validate_update")
    op.execute("DROP TRIGGER IF EXISTS trg_audit_details_validate_insert")
    op.drop_index("ix_audit_logs_user_created", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_table("guest_usage")
    op.drop_index("ix_password_reset_tokens_user_id", table_name="password_reset_tokens")
    op.drop_table("password_reset_tokens")
    op.drop_index("ix_email_verification_tokens_user_id", table_name="email_verification_tokens")
    op.drop_table("email_verification_tokens")
    op.drop_index("ix_recovery_codes_user_id", table_name="recovery_codes")
    op.drop_table("recovery_codes")
    op.drop_table("two_factor_methods")
    op.drop_index("ix_sessions_user_expiry", table_name="sessions")
    op.drop_index("ix_sessions_user_id", table_name="sessions")
    op.drop_table("sessions")
    op.drop_index("ix_invitations_email_status", table_name="invitations")
    op.drop_table("invitations")
    op.drop_index("ix_oauth_accounts_user_id", table_name="oauth_accounts")
    op.drop_table("oauth_accounts")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
