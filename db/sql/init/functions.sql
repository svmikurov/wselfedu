-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Defines functions

BEGIN;

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


-- Trigger function for created_at, updated_at fields
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

-- Applying Changes
COMMIT;
