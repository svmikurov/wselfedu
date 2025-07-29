"""Initial migration to create database schemas and set permissions.

For each schema:
1. Creates the schema with IF NOT EXISTS
2. Grants all privileges to the application database user
3. Sets the owner to the application database user
"""

from django.apps.registry import Apps
from django.db import migrations, connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from utils.load import get_db_user

# List of schemas to create
SCHEMAS: list[str] = [
    'lang',
    'main',
    'math',
    'triggers',
    'users',
]


def create_schema(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Create database schemas and set permissions."""
    db_user = get_db_user()
    quoted_user = connection.ops.quote_name(db_user)

    for schema in SCHEMAS:
        schema_editor.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {schema};
        GRANT ALL PRIVILEGES ON SCHEMA {schema} TO {quoted_user};
        ALTER SCHEMA {schema} OWNER TO {quoted_user};
        """)


def reverse_schema(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Reverse operation: drop all created schemas."""
    for schema in SCHEMAS:
        schema_editor.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE;')


class Migration(migrations.Migration):
    """Initial database schema creation migration."""

    run_before = [
        ('contenttypes', '0001_initial'),  # Run before Django's initial migrations
    ]

    # No dependencies since this is an initial migration
    dependencies = [
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # Database operations
            database_operations=[
                migrations.RunPython(
                    code=create_schema,
                    reverse_code=reverse_schema,
                ),
            ],
            # No state operations needed (pure DB change)
            state_operations=[],
        ),
    ]
