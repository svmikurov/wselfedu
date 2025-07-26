-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Updated: 2025-07-25
-- Description: Defines procedure for balance update with transaction

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

COMMIT;