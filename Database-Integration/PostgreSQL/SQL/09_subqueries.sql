-- Create departments table
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create employees table
CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER,
    salary NUMERIC(10, 2),
    active BOOLEAN DEFAULT TRUE
);

-- Insert departments
INSERT INTO departments (name)
VALUES
('Backend'),
('Frontend'),
('Data'),
('DevOps');

-- Insert employees
INSERT INTO employees
(name, department_id, salary, active)
VALUES
('Gaurav Panwar', 1, 85000, TRUE),
('Rahul Sharma', 1, 65000, TRUE),
('Ankit Verma', 1, 48000, FALSE),
('Priya Singh', 2, 72000, TRUE),
('Neha Gupta', 2, 58000, TRUE),
('Riya Mehta', 3, 90000, TRUE),
('Karan Singh', 3, 70000, TRUE);

-- ------------------
-- Scalar Subquery
-- ------------------

SELECT
    name,
    salary
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);

-- ------------------
-- Subquery with MAX
-- ------------------

SELECT
    name,
    salary
FROM employees
WHERE salary = (
    SELECT MAX(salary)
    FROM employees
);

-- ------------------
-- Subquery with MIN
-- ------------------

SELECT
    name,
    salary
FROM employees
WHERE salary = (
    SELECT MIN(salary)
    FROM employees
);

-- ------------------
-- IN with Subquery
-- ------------------

SELECT
    name,
    department_id
FROM employees
WHERE department_id IN (
    SELECT id
    FROM departments
    WHERE name IN ('Backend', 'Data')
);

-- ------------------
-- NOT IN with Subquery
-- ------------------

SELECT
    name,
    department_id
FROM employees
WHERE department_id NOT IN (
    SELECT id
    FROM departments
    WHERE name = 'Backend'
);

-- ------------------
-- EXISTS
-- ------------------

SELECT
    d.id,
    d.name
FROM departments AS d
WHERE EXISTS (
    SELECT 1
    FROM employees AS e
    WHERE e.department_id = d.id
);

-- ------------------
-- NOT EXISTS
-- ------------------

SELECT
    d.id,
    d.name
FROM departments AS d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees AS e
    WHERE e.department_id = d.id
);

-- ------------------
-- Correlated Subquery
-- ------------------

SELECT
    e.name,
    e.department_id,
    e.salary
FROM employees AS e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees AS e2
    WHERE e2.department_id = e.department_id
);

-- ------------------
-- Subquery in FROM
-- ------------------

SELECT
    department_id,
    average_salary
FROM (
    SELECT
        department_id,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
) AS department_stats;

-- ------------------
-- Subquery in SELECT
-- ------------------

SELECT
    name,
    salary,
    (
        SELECT AVG(salary)
        FROM employees
    ) AS company_average_salary
FROM employees;

-- ------------------
-- Subquery with WHERE and Aggregation
-- ------------------

SELECT
    name,
    salary,
    department_id
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE active = TRUE
);

-- ------------------
-- Subquery with DISTINCT
-- ------------------

SELECT
    name,
    department_id
FROM employees
WHERE department_id IN (
    SELECT DISTINCT department_id
    FROM employees
    WHERE salary > 70000
);

-- ------------------
-- JOIN vs Subquery Style
-- ------------------

SELECT
    e.name,
    d.name AS department
FROM employees AS e
JOIN departments AS d
ON e.department_id = d.id
WHERE d.name = 'Backend';