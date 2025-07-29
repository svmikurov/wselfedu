"""Migration to create stored procedure for incrementing user rewards.

Creates PostgreSQL stored procedure `increment_user_reward()` that:
1. Records reward transaction in the appropriate app schema
2. Updates user balance atomically
"""

from django.db import migrations

# SQL for creating the procedure for incrementing user rewards
PROCEDURE_SQL = """
BEGIN;
-- Procedure to reward bonus to user
-- For example: CALL increment_user_reward(123, 100.50, 'math');
CREATE OR REPLACE PROCEDURE increment_user_reward(
    p_user_id INTEGER,
    p_amount DECIMAL,
    p_app_name VARCHAR(50)
) LANGUAGE plpgsql AS $$
-- Declare to fetch app schema name
DECLARE
    v_schema_name TEXT;
    v_table_name TEXT := 'transaction';
BEGIN
    -- Get app schema for transaction
    SELECT schema_name INTO v_schema_name
    FROM main.app
    WHERE schema_name = p_app_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Unknown app: %', p_app_name;
    END IF;

    -- Add transaction
    EXECUTE format(
        'INSERT INTO %I.%I (user_id, amount, type) VALUES ($1, $2, ''reward'')',
        v_schema_name, v_table_name
    ) USING p_user_id, p_amount;

    -- Update balance
    IF EXISTS (SELECT 1 FROM users.balance WHERE user_id = p_user_id) THEN
        UPDATE users.balance
        SET total = total + p_amount, updated_at = NOW()
        WHERE user_id = p_user_id;
    ELSE
        INSERT INTO users.balance (user_id, total, created_at, updated_at)
        VALUES (p_user_id, p_amount, NOW(), NOW());
    END IF;
END;
$$;
"""

# SQL for reverse migration
REVERSE_SQL = """
DROP PROCEDURE IF EXISTS increment_user_reward;
"""


class Migration(migrations.Migration):
    """Migration to create user reward increment procedure."""

    dependencies = [
        ('pg_utils', '0003_create_trg_create_with_update_timestamp'),  # Previous migration
        ('users', '0002_create_balance'),  # Ensure balance table exists
        ('lang', '0002_create_transaction'),  # Ensure transaction tables exist
        ('math', '0002_create_transaction'), # Ensure transaction tables exist
    ]

    operations = [
        migrations.RunSQL(
            sql=PROCEDURE_SQL,
            reverse_sql=REVERSE_SQL,
        ),
    ]
