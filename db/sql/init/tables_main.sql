-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Updated: 2025-07-26
-- Description: Defines main app schemas

BEGIN;

-- Base exercise table
CREATE TABLE main.exercise (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Base reward transaction table
CREATE TABLE main.transaction (
    id INT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL (11, 2) NOT NULL,
    type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users.customuser(id)
        ON DELETE CASCADE
);

COMMIT;