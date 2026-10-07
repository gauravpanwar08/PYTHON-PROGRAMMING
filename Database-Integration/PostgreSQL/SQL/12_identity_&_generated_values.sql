-- ============================================================
-- PostgreSQL Identity & Generated Values
-- ============================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS users;

-- --------------------------------------------------
-- Identity Column
-- --------------------------------------------------

CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- --------------------------------------------------
-- Automatic Identity Values
-- --------------------------------------------------

INSERT INTO users (name, email)
VALUES
    ('Gaurav', 'gaurav@example.com'),
    ('Rahul', 'rahul@example.com'),
    ('Priya', 'priya@example.com');


-- View Identity Values

SELECT * FROM users;

-- --------------------------------------------------
-- Identity With Custom Start Value
-- --------------------------------------------------

CREATE TABLE order_items (
    id INTEGER GENERATED ALWAYS AS IDENTITY
        (START WITH 1000 INCREMENT BY 1)
        PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_price NUMERIC(10, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED
);


-- Insert Source Values

INSERT INTO order_items (
    product_name,
    quantity,
    unit_price
)
VALUES
    ('Keyboard', 2, 1500.00),
    ('Mouse', 3, 800.00),
    ('Monitor', 1, 12000.00);


-- View Generated Values

SELECT
    id,
    product_name,
    quantity,
    unit_price,
    total_price
FROM order_items
ORDER BY id;


-- Update Source Columns

UPDATE order_items
SET quantity = 5
WHERE id = 1000;


-- Generated Column Updates Automatically

SELECT
    id,
    product_name,
    quantity,
    unit_price,
    total_price
FROM order_items
WHERE id = 1000;
