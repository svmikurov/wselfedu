"""Migration for base Exercise model in PostgreSQL.

Creates the base exercise table that will be inherited by specialized
exercise tables in other schemas.
"""

from django.db import migrations

# SQL for creating the base exercise table
CREATE_TABLE_SQL = """
CREATE TABLE main.exercise (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);
"""

# SQL for reverse migration
DROP_TABLE_SQL = """
DROP TABLE IF EXISTS main.exercise CASCADE;
"""


class Migration(migrations.Migration):
    """Migration to create the base exercise table."""

    dependencies = [
        ('pg_utils', '0001_create_schemas'),  # Ensures 'main' schema exists
    ]

    operations = [
        migrations.RunSQL(
            sql=CREATE_TABLE_SQL,
            reverse_sql=DROP_TABLE_SQL,
        ),
    ]
