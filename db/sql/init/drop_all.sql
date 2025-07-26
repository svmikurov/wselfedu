-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-26
-- Description: Drop role and DB

-- Drop existing DB
DROP DATABASE IF EXISTS :db_name;

-- Drop role
DROP ROLE IF EXISTS :db_user;