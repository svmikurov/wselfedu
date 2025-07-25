-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Description: Database role creation

-- Drop existing role
--DROP ROLE IF EXISTS sv;

-- Create user
CREATE USER sv WITH password 'password';
ALTER ROLE sv SET client_encoding TO 'utf8';
ALTER ROLE sv SET default_transaction_isolation TO 'read committed';
ALTER ROLE sv SET timezone TO 'UTC';
ALTER USER sv CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE wse_db TO sv;