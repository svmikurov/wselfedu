-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Date: 2025-07-25
-- Description: Defines triggers for Math app

BEGIN;

CREATE TRIGGER trg_transaction_update_timestamp
BEFORE INSERT OR UPDATE ON math.transaction
FOR EACH ROW
EXECUTE FUNCTION triggers.create_timestamp();

COMMIT;