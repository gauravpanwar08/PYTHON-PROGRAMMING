-- ==================================================
-- PostgreSQL Schemas
-- Purpose: Organize database objects into schemas
-- ==================================================

-- Create schemas

CREATE SCHEMA IF NOT EXISTS app_data;
CREATE SCHEMA IF NOT EXISTS billing;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create tables inside schemas

CREATE TABLE app_data.customers (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE billing.invoices (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES app_data.customers(id),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE analytics.daily_sales (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sale_date DATE NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0
);

-- Insert sample customers

INSERT INTO app_data.customers (name, email)
VALUES
    ('Rahul', 'rahul@example.com'),
    ('Priya', 'priya@example.com');

-- Insert sample invoices

INSERT INTO billing.invoices (customer_id, amount, status)
VALUES
    (1, 2500, 'paid'),
    (2, 1800, 'pending');

-- Insert sample analytics data

INSERT INTO analytics.daily_sales (sale_date, total_amount)
VALUES
    (CURRENT_DATE - 1, 2500),
    (CURRENT_DATE, 1800);

-- Query tables using schema-qualified names

SELECT * FROM app_data.customers;

SELECT * FROM billing.invoices;

SELECT * FROM analytics.daily_sales;

-- Join tables across schemas

SELECT
    c.name,
    i.amount,
    i.status
FROM app_data.customers AS c
JOIN billing.invoices AS i
    ON i.customer_id = c.id
ORDER BY c.name;

-- Inspect existing schemas

SELECT schema_name
FROM information_schema.schemata
ORDER BY schema_name;

-- Inspect tables in application schemas

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema IN ('app_data', 'billing', 'analytics')
  AND table_type = 'BASE TABLE'
ORDER BY table_schema, table_name;

-- Inspect the current search path

SHOW search_path;

-- Set the search path for this session

SET search_path TO app_data, public;

SELECT * FROM customers;

-- Reset the search path

RESET search_path;
