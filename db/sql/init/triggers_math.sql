-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Contains triggers for Math app

-- Starting a transaction
BEGIN;

-- Update datetime fields
CREATE TRIGGER trg_update_timestamp
BEFORE INSERT OR UPDATE ON math.exercise
FOR EACH ROW
EXECUTE FUNCTION triggers.update_timestamp();

-- Applying changes
COMMIT;