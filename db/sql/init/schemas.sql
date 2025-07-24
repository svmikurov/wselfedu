-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Contains schemas (not for tables)

-- Starting a transaction
BEGIN;

-- Schema for trigger functions
CREATE SCHEMA triggers;
GRANT ALL PRIVILEGES ON SCHEMA triggers TO sv;
ALTER SCHEMA triggers OWNER TO sv;

-- Applying Changes
COMMIT;