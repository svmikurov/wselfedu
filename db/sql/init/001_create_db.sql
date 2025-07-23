-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Description: Postgres DB creating

-- Drop existing DB
DROP DATABASE IF EXISTS wse_db;

-- Create DB
CREATE DATABASE wse_db WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;