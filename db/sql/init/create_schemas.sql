-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-24
-- Updated: 2025-07-26
-- Description: Defines schemas

\connect wse_db

BEGIN;

-- Tables

-- Schema for main app tables
-- Contains base tables to inherit
CREATE SCHEMA main;
GRANT ALL PRIVILEGES ON SCHEMA main TO sv;
ALTER SCHEMA main OWNER TO sv;

-- Schema for Users app tables
CREATE SCHEMA users;
GRANT ALL PRIVILEGES ON SCHEMA users TO sv;
ALTER SCHEMA users OWNER TO sv;

-- Schema for Math app tables
CREATE SCHEMA math;
GRANT ALL PRIVILEGES ON SCHEMA math TO sv;
ALTER SCHEMA math OWNER TO sv;

-- Schema for Lang app tables
CREATE SCHEMA lang;
GRANT ALL PRIVILEGES ON SCHEMA lang TO sv;
ALTER SCHEMA lang OWNER TO sv;

-- Functions

-- Schema for trigger functions
CREATE SCHEMA triggers;
GRANT ALL PRIVILEGES ON SCHEMA triggers TO sv;
ALTER SCHEMA triggers OWNER TO sv;

COMMIT;