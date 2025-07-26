-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Updated: 2025-07-26
-- Description: Database role creation

-- Create role
CREATE ROLE :db_user;
ALTER ROLE :db_user PASSWORD :'db_password';
ALTER ROLE :db_user LOGIN;
ALTER ROLE :db_user SET client_encoding TO 'utf8';
ALTER ROLE :db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE :db_user SET timezone TO 'UTC';
ALTER ROLE :db_user CREATEDB;