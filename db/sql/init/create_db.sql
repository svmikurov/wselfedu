-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Updated: 2025-07-26
-- Description: Postgres DB creating

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