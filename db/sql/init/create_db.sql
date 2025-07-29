-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-29
-- Description: Create role and DB, drop if exists

-- Drop existing DB
DROP DATABASE IF EXISTS :db_name;

-- Drop role
DROP ROLE IF EXISTS :db_user;

-- Create role
CREATE ROLE :db_user;
ALTER ROLE :db_user PASSWORD :'db_password';
ALTER ROLE :db_user LOGIN;
ALTER ROLE :db_user SET client_encoding TO 'utf8';
ALTER ROLE :db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE :db_user SET timezone TO 'UTC';
ALTER ROLE :db_user CREATEDB;

-- Set role
SET ROLE :db_user;

-- Create DB
CREATE DATABASE :db_name WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grand privileges for created DB
GRANT ALL PRIVILEGES ON DATABASE :db_name TO :db_user;