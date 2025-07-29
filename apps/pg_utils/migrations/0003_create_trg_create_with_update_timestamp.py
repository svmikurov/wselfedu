"""Migration to create timestamp management trigger.

Creates:
1. PostgreSQL function `triggers.create_with_update_timestamp()` that:
   - Sets `created_at` to current time on INSERT if NULL
   - Automatically updates `updated_at` on INSERT/UPDATE
   - Prevents modification of `created_at` on UPDATE
2. Trigger `trg_create_with_update_timestamp` that applies the function
"""
from django.db import migrations
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

# Tables to apply the trigger to
TABLES = [
    'lang.exercise',
    'math.exercise',
]

# SQL for creating the timestamp management function
FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION triggers.create_with_update_timestamp()
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
        IF NEW.created_at IS NULL THEN
            NEW.created_at = NOW();
        END IF;

        NEW.updated_at = NOW();

    -- Check datatime changes only for UPDATE operations
    ELSIF TG_OP = 'UPDATE' THEN
        -- Checking the created_at field
        IF NEW.created_at IS DISTINCT FROM OLD.created_at THEN
            error_message := error_message || 'The created_at field cannot be edited. ';
            violation_details := violation_details || format(
                'Trying to change the created_at from %s to %s. ',
                OLD.created_at,
                NEW.created_at
            );
        END IF;

        -- Update only updated_at field
        NEW.updated_at = NOW();

        -- Build error messaged
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
REVERSE_FUNCTION_SQL = """
DROP FUNCTION IF EXISTS triggers.create_with_update_timestamp;
"""


def apply_triggers(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Apply the timestamp trigger to all specified tables."""
    for table in TABLES:
        schema_editor.execute(f"""
        CREATE TRIGGER trg_create_with_update_timestamp
        BEFORE INSERT OR UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION triggers.create_with_update_timestamp();
        """)


def drop_triggers(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Remove triggers during migration reversal."""
    for table in TABLES:
        schema_editor.execute(f"""
        DROP TRIGGER IF EXISTS trg_create_with_update_timestamp ON {table};
        """)


class Migration(migrations.Migration):
    """Migration to create and apply timestamp management trigger."""

    dependencies = [
        ('pg_utils', '0002_create_trg_create_timestamp'),  # Previous migration
        ('lang', '0002_create_transaction'),  # Ensure tables exist
        ('math', '0002_create_transaction'),  # Ensure tables exist
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # Database operations
            database_operations=[
                # Create the timestamp function
                migrations.RunSQL(
                    sql=FUNCTION_SQL,
                    reverse_sql=REVERSE_FUNCTION_SQL,
                ),
                # Apply triggers to tables
                migrations.RunPython(
                    code=apply_triggers,
                    reverse_code=drop_triggers,
                ),
            ],
            # No state operations needed (pure database change)
            state_operations=[],
        ),
    ]
