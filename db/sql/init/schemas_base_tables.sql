-- Version: 0.1.0
-- Autor: Sergei Mikurov
-- Date: 2025-07-23
-- Description: Contains base schemas

-- Starting a transaction
BEGIN;

-- Base exercise table
CREATE TABLE base.exercise (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Base reward transaction table
CREATE TABLE base.transaction (
    id INT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL (11, 2) NOT NULL,
    type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    -- Add into derived tables also
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users.customuser(id)
        ON DELETE CASCADE
);

-- Applying Changes
COMMIT;