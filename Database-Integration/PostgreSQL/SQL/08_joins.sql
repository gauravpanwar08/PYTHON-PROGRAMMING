
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
    manager_id INTEGER,
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
(name, department_id, manager_id, salary, active)
VALUES
('Gaurav Panwar', 1, NULL, 85000, TRUE),
('Rahul Sharma', 2, 1, 65000, TRUE),
('Ankit Verma', 1, 1, 48000, FALSE),
('Priya Singh', 3, 1, 72000, TRUE),
('Aman Kumar', NULL, 1, 45000, TRUE);

-- ------------------
-- INNER JOIN
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id;

-- ------------------
-- LEFT JOIN
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id;

-- ------------------
-- RIGHT JOIN
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
RIGHT JOIN departments AS d
ON e.department_id = d.id;

-- ------------------
-- FULL OUTER JOIN
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
FULL OUTER JOIN departments AS d
ON e.department_id = d.id;

-- ------------------
-- CROSS JOIN
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
CROSS JOIN departments AS d;

-- ------------------
-- LEFT JOIN with WHERE
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
WHERE e.active = TRUE;

-- ------------------
-- LEFT JOIN with condition in ON
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
AND d.name = 'Backend';

-- ------------------
-- Self JOIN
-- ------------------

SELECT
    e.name AS employee,
    m.name AS manager
FROM employees AS e
LEFT JOIN employees AS m
ON e.manager_id = m.id;

-- ------------------
-- JOIN with Filtering
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department,
    e.salary
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id
WHERE e.salary > 60000;

-- ------------------
-- JOIN with ORDER BY
-- ------------------

SELECT
    e.name AS employee,
    d.name AS department,
    e.salary
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
ORDER BY e.salary DESC;

-- ------------------
-- JOIN with Aggregation
-- ------------------

SELECT
    d.name AS department,
    COUNT(e.id) AS employee_count,
    COALESCE(SUM(e.salary), 0) AS total_salary,
    COALESCE(AVG(e.salary), 0) AS average_salary
FROM departments AS d
LEFT JOIN employees AS e
ON e.department_id = d.id
GROUP BY d.id, d.name
ORDER BY total_salary DESC;

