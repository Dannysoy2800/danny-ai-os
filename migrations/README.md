# Authentication database migrations

The authentication database schema is managed by Alembic.

## Fresh database

Install dependencies and initialize the schema:

```bash
python -m pip install -r requirements.txt
python -m database.init_db
```

The command reads `PAI_DB_PATH` (default:
`.personal_ai_os/auth.sqlite3`) and upgrades the database to the latest
revision. Running it again is safe for a database already managed by Alembic.

## Creating a schema revision

After changing SQLAlchemy models, generate and review a migration:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Review generated operations carefully, especially SQLite constraints,
foreign keys, indexes, and audit triggers. Never edit an already-applied
revision; create a new revision instead.

## Existing unversioned databases

The initializer intentionally refuses to migrate a database that already
contains application tables but has no `alembic_version` table. It does not
automatically stamp, drop, or recreate such a database.

Before adopting an existing database:

1. Stop application processes that could write to it.
2. Make and verify a separate backup.
3. Compare its tables, columns, indexes, constraints, foreign keys, and audit
   triggers with revision `0001_auth_schema`.
4. Use a separately reviewed adoption procedure to stamp the baseline only
   after the schema is proven equivalent.
5. Run the migration tests against a copy of the database before production use.

This repository does not yet automate that adoption procedure. The refusal is
intentional to avoid data loss or silently accepting schema drift.

## Downgrade

Alembic downgrade operations can remove application tables and data. Use them
only against disposable test databases or after a verified backup:

```bash
alembic downgrade base
```
