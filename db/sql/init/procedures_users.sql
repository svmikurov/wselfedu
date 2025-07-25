-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Updated: 2025-07-25
-- Description: Defines procedure for balance update with transaction

BEGIN;

-- Procedure to reward bonus to user
-- For example: CALL add_bonus(123, 100.50, 'math');
CREATE OR REPLACE PROCEDURE add_bonus(
    p_user_id INTEGER,
    p_amount DECIMAL,
    p_app_name VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Add transaction
    IF p_app_name = 'math' THEN
        INSERT INTO math.transaction (user_id, amount, type)
        VALUES (p_user_id, p_amount, 'reward');
    ELSIF p_app_name = 'lang' THEN
        INSERT INTO lang.transaction (user_id, amount, type)
        VALUES (p_user_id, p_amount, 'reward');
    ELSE
        RAISE EXCEPTION 'Unknown app: % ', p_app_name;
    END IF;

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