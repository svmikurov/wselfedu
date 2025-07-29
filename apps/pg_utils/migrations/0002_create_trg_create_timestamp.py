"""Migration to create trigger for `created_at` table field.

Creates:
1. PostgreSQL function `triggers.create_timestamp()` that:
   - Automatically sets `created_at` on INSERT if NULL
   - Prevents modification of `created_at` on UPDATE
2. Trigger `trg_create_timestamp` that applies the function
"""

from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

# Tables to apply the trigger to
TABLES: list[str] = [
    'lang.transaction',
    'math.transaction',
]

# SQL for creating the trigger function
FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION triggers.create_timestamp()
RETURNS TRIGGER AS $$
DECLARE
    error_message TEXT;
    violation_details TEXT;
    current_user_name TEXT;
BEGIN
    SELECT current_user INTO current_user_name;

    error_message := '';
    violation_details := '';

    IF TG_OP = 'INSERT' THEN
        IF NEW.created_at IS NULL  THEN
            NEW.created_at = NOW();
        END IF;
    END IF;

    IF TG_OP = 'UPDATE' THEN
        IF NEW.created_at IS DISTINCT FROM OLD.created_at THEN
            error_message := error_message || 'The created_at field cannot be edited. ';
            violation_details := violation_details || format(
                'Trying to change the created_at from %s to %s. ',
                OLD.created_at,
                NEW.created_at
            );
        END IF;

        -- Build error message
        IF error_message <> '' THEN
            RAISE LOG 'Attempted to modify protected fields. User: %, Table: %, Record ID: %, Details: %',
            current_user_name,
            TG_TABLE_NAME,
            NEW.id,
            violation_details;

            -- Generating a full error message
            RAISE EXCEPTION 'Violation of the rules for changing data: %', error_message
            USING HINT = 'To modify these fields, use a special API method',
                  DETAIL = violation_details,
                  ERRCODE = 'restrict_violation';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

# SQL for reverting the function creation
REVERSE_FUNCTION_SQL = 'DROP FUNCTION IF EXISTS triggers.create_timestamp;'


def apply_trigger(
    apps: Apps,
    schema_creator: BaseDatabaseSchemaEditor,
) -> None:
    """Apply the timestamp trigger to all specified tables."""
    for table in TABLES:
        schema_creator.execute(f"""
        CREATE TRIGGER trg_create_timestamp
        BEFORE INSERT OR UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION triggers.create_timestamp();
        """)


def drop_triggers(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Reverse function for removing triggers."""
    for table in TABLES:
        schema_editor.execute(f"""
        DROP TRIGGER IF EXISTS trg_create_timestamp ON {table};
        """)


class Migration(migrations.Migration):
    """Migration to create and apply timestamp protection trigger."""

    dependencies = [
        ('pg_utils', '0001_create_schemas'),  # Previous migration
        ('lang', '0001_create_exercise'),  # Ensure tables exist
        ('math', '0001_create_exercise'),  # Ensure tables exist
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # Database operations
            database_operations=[
                # Create the function
                migrations.RunSQL(
                    sql=FUNCTION_SQL,
                    reverse_sql=REVERSE_FUNCTION_SQL,
                ),
                # Apply triggers to tables
                migrations.RunPython(
                    code=apply_trigger,
                    reverse_code=drop_triggers,
                ),
            ],
            # No state operations needed (pure DB change)
            state_operations=[],
        ),
    ]
