"""Initial migration for base Transaction model in PostgreSQL.

Creates the base exercise table that will be inherited by specialized
transaction tables in other schemas.
"""

from django.db import migrations

# SQL for creating the base transaction table
CREATE_TABLE_SQL = """
CREATE TABLE main.transaction (
    id INT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL (11, 2) NOT NULL,
    type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users.customuser(id)
        ON DELETE CASCADE
);
"""

# SQL for reverse migration
DROP_TABLE_SQL = """
DROP TABLE IF EXISTS main.transaction CASCADE;
"""


class Migration(migrations.Migration):
    """Migration to create the base transaction table in main schema."""

    dependencies = [
        ('main', '0001_create_base_exercise'),  # Previous migration
        ('pg_utils', '0001_create_schemas'),  # Ensures 'main' schema exists
    ]

    operations = [
        migrations.RunSQL(
            sql=CREATE_TABLE_SQL,
            reverse_sql=DROP_TABLE_SQL,
        ),
    ]
