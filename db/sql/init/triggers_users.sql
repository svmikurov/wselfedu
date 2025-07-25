-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Update: 2025-07-25
-- Description: Defines triggers for Math app

BEGIN;

CREATE TRIGGER trg_users_timestamp
BEFORE INSERT OR UPDATE ON users.customuser
FOR EACH ROW
EXECUTE FUNCTION triggers.create_with_update_timestamp();

COMMIT;