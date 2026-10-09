-- ============================================================
-- PostgreSQL Views
-- ============================================================

DROP MATERIALIZED VIEW IF EXISTS department_salary_summary;
DROP VIEW IF EXISTS employee_department_details;
DROP VIEW IF EXISTS active_employees;
DROP VIEW IF EXISTS employee_public;

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;


-- Create Tables

CREATE TABLE departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary > 0),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    department_id INTEGER REFERENCES departments(id)
);


-- Insert Sample Data

INSERT INTO departments (name)
VALUES
    ('Engineering'),
    ('HR'),
    ('Finance');

INSERT INTO employees (
    name,
    email,
    salary,
    active,
    department_id
)
VALUES
    ('Gaurav', 'gaurav@example.com', 75000, TRUE, 1),
    ('Rahul', 'rahul@example.com', 65000, TRUE, 1),
    ('Priya', 'priya@example.com', 60000, FALSE, 2),
    ('Aman', 'aman@example.com', 55000, TRUE, 3);

-- ----------------------------
-- Create a Basic View
-- ----------------------------

CREATE VIEW employee_public AS
SELECT id, name, email
FROM employees;

SELECT * FROM employee_public;

-- ----------------------------
-- Create a Filtered View
-- ----------------------------

CREATE VIEW active_employees AS
SELECT id, name, salary, department_id
FROM employees
WHERE active = TRUE;

SELECT * FROM active_employees;

-- ----------------------------
-- Replace View Definition
-- ----------------------------

CREATE OR REPLACE VIEW employee_public AS
SELECT id, name, email, department_id
FROM employees;

SELECT * FROM employee_public;

-- ----------------------------
-- Create a View With JOIN
-- ----------------------------

CREATE VIEW employee_department_details AS
SELECT
    e.id AS employee_id,
    e.name AS employee_name,
    d.name AS department_name,
    e.salary
FROM employees AS e
LEFT JOIN departments AS d
    ON e.department_id = d.id;

SELECT * FROM employee_department_details;

-- -----------------------------------------
-- Query a View With Additional Filtering
-- -----------------------------------------

SELECT *
FROM employee_department_details
WHERE salary >= 60000
ORDER BY salary DESC;

-- ----------------------------
-- Create a Materialized View
-- ----------------------------

CREATE MATERIALIZED VIEW department_salary_summary AS
SELECT
    d.name AS department_name,
    COUNT(e.id) AS employee_count,
    COALESCE(AVG(e.salary), 0) AS average_salary
FROM departments AS d
LEFT JOIN employees AS e
    ON e.department_id = d.id
GROUP BY d.id, d.name;

SELECT * FROM department_salary_summary;

-- ----------------------------
-- Refresh Materialized 
-- ----------------------------

UPDATE employees
SET salary = 80000
WHERE id = 1;

REFRESH MATERIALIZED VIEW department_salary_summary;

SELECT * FROM department_salary_summary;

-- ----------------------------
-- Drop Views
-- ----------------------------

DROP MATERIALIZED VIEW department_salary_summary;
DROP VIEW employee_department_details;
DROP VIEW active_employees;
DROP VIEW employee_public;
