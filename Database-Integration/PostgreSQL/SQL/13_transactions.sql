-- ============================================================
-- PostgreSQL Transactions - ACID Property
-- ============================================================

DROP TABLE IF EXISTS accounts;

-- Create Table

CREATE TABLE accounts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_holder TEXT NOT NULL,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0)
);


-- Insert Initial Data

INSERT INTO accounts (account_holder, balance)
VALUES
    ('Gaurav', 10000.00),
    ('Rahul', 5000.00);

SELECT * FROM accounts;

-- ------------------------------------
-- Successful Transaction
-- ------------------------------------

BEGIN;

UPDATE accounts
SET balance = balance - 2000
WHERE id = 1;

UPDATE accounts
SET balance = balance + 2000
WHERE id = 2;

COMMIT;

SELECT * FROM accounts;

-- ------------------------------------
-- Transaction With ROLLBACK
-- ------------------------------------

BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE id = 1;

UPDATE accounts
SET balance = balance + 1000
WHERE id = 2;

ROLLBACK;

SELECT * FROM accounts;

-- ------------------------------------
-- SAVEPOINT
-- ------------------------------------

BEGIN;

UPDATE accounts
SET balance = balance - 500
WHERE id = 1;

SAVEPOINT after_deduction;

UPDATE accounts
SET balance = balance + 500
WHERE id = 2;

ROLLBACK TO SAVEPOINT after_deduction;

COMMIT;

SELECT * FROM accounts;

-- ------------------------------------
-- Transaction With Constraint Failure
-- ------------------------------------

BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE id = 1;

UPDATE accounts
SET balance = -500
WHERE id = 2;

ROLLBACK;

SELECT * FROM accounts;
