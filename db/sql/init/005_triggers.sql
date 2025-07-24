-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Defines triggers

-- Starting a transaction
BEGIN;

-- Create update timestamp trigger on base exercise table
CREATE TRIGGER base_exercise
BEFORE UPDATE ON math_exercise
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Applying changes
COMMIT;