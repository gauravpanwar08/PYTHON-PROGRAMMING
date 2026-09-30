-- Create employees table
CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email TEXT,
    salary NUMERIC(10, 2),
    department VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO employees (name, email, salary, department, is_active)
VALUES
    ('Rahul', 'rahul@example.com', 50000, 'Backend', TRUE),
    ('Aman', 'aman@example.com', 65000, 'Frontend', TRUE),
    ('Priya', NULL, 70000, 'Backend', TRUE),
    ('Neha', 'neha@example.com', 45000, 'HR', FALSE),
    ('Ankit', 'ankit@example.com', 80000, 'Backend', TRUE),
    ('Riya', NULL, 55000, 'HR', TRUE),
    ('Amit', 'amit@example.com', 60000, 'Frontend', FALSE);

-- Select all columns
SELECT *
FROM employees;

-- Select specific columns
SELECT name, salary
FROM employees;

-- Filter using WHERE
SELECT *
FROM employees
WHERE salary > 50000;

-- Comparison operators
SELECT *
FROM employees
WHERE salary >= 60000;

-- AND
SELECT *
FROM employees
WHERE salary > 50000
AND is_active = TRUE;

-- OR
SELECT *
FROM employees
WHERE department = 'Backend'
OR department = 'Frontend';

-- NOT
SELECT *
FROM employees
WHERE NOT is_active;

-- IN
SELECT *
FROM employees
WHERE department IN ('Backend', 'HR');

-- NOT IN
SELECT *
FROM employees
WHERE department NOT IN ('HR');

-- BETWEEN
SELECT *
FROM employees
WHERE salary BETWEEN 50000 AND 70000;

-- NOT BETWEEN
SELECT *
FROM employees
WHERE salary NOT BETWEEN 50000 AND 70000;

-- LIKE
SELECT *
FROM employees
WHERE name LIKE 'A%';

-- LIKE with contains pattern
SELECT *
FROM employees
WHERE name LIKE '%an%';

-- ILIKE
SELECT *
FROM employees
WHERE name ILIKE 'rahul';

-- IS NULL
SELECT *
FROM employees
WHERE email IS NULL;

-- IS NOT NULL
SELECT *
FROM employees
WHERE email IS NOT NULL;

-- DISTINCT
SELECT DISTINCT department
FROM employees;

-- ORDER BY ascending
SELECT *
FROM employees
ORDER BY salary ASC;

-- ORDER BY descending
SELECT *
FROM employees
ORDER BY salary DESC;

-- Multiple-column sorting
SELECT *
FROM employees
ORDER BY department ASC, salary DESC;

-- LIMIT
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 3;

-- OFFSET
SELECT *
FROM employees
ORDER BY id
OFFSET 3;

-- LIMIT with OFFSET
SELECT *
FROM employees
ORDER BY id
LIMIT 3
OFFSET 2;

-- Combined filtering, sorting and limiting
SELECT name, salary, department
FROM employees
WHERE salary >= 50000
AND is_active = TRUE
ORDER BY salary DESC
LIMIT 3;