-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Updated: 2025-07-25
-- Description: Defines triggers for Lang app

BEGIN;

CREATE TRIGGER trg_exercise_timestamp
BEFORE INSERT OR UPDATE ON lang.exercise
FOR EACH ROW
EXECUTE FUNCTION triggers.create_with_update_timestamp();

CREATE TRIGGER trg_transaction_timestamp
BEFORE INSERT OR UPDATE ON lang.transaction
FOR EACH ROW
EXECUTE FUNCTION triggers.create_timestamp();

COMMIT;