-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Description: Contains schemas (not for tables)

-- Starting a transaction
BEGIN;

-- Schema for base tables
CREATE SCHEMA base;
GRANT ALL PRIVILEGES ON SCHEMA base TO sv;
ALTER SCHEMA base OWNER TO sv;

-- Schema for Math app tables
CREATE SCHEMA math;
GRANT ALL PRIVILEGES ON SCHEMA math TO sv;
ALTER SCHEMA math OWNER TO sv;

-- Schema for Lang app tables
CREATE SCHEMA lang;
GRANT ALL PRIVILEGES ON SCHEMA lang TO sv;
ALTER SCHEMA lang OWNER TO sv;

-- Schema for trigger functions
CREATE SCHEMA triggers;
GRANT ALL PRIVILEGES ON SCHEMA triggers TO sv;
ALTER SCHEMA triggers OWNER TO sv;

-- Applying Changes
COMMIT;