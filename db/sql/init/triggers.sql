-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Contains triggers

-- Starting a transaction
BEGIN;

-- Create update timestamp trigger on base exercise table
CREATE TRIGGER trg_update_timestamp
BEFORE UPDATE ON math_exercise
FOR EACH ROW
EXECUTE FUNCTION triggers.update_timestamp();

-- Applying changes
COMMIT;