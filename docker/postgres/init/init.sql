-- Version: 0.1.1
-- Author: Sergei Mikurov
-- Date: 2026-01-15
-- Description: Create role and DB

-- Create role if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = :'db_user') THEN
        CREATE ROLE :db_user;
    END IF;
END
$$;

-- Set up a role
ALTER ROLE :db_user PASSWORD :'db_password';
ALTER ROLE :db_user LOGIN;
ALTER ROLE :db_user SET client_encoding TO 'utf8';
ALTER ROLE :db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE :db_user SET timezone TO 'UTC';
ALTER ROLE :db_user CREATEDB;

-- Create a database if it does not exist
SELECT 'CREATE DATABASE ' || :'db_name' || ' WITH
    ENCODING = ''UTF8''
    LC_COLLATE = ''en_US.UTF-8''
    LC_CTYPE = ''en_US.UTF-8''
    TEMPLATE = template0'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'db_name')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE :db_name TO :db_user;

-- Make owner
ALTER DATABASE :db_name OWNER TO :db_user;