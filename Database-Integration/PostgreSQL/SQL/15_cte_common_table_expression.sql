-- ============================================================
-- PostgreSQL CTEs - Common Table Expression
-- ============================================================

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
    department_id INTEGER REFERENCES departments(id),
    manager_id INTEGER REFERENCES employees(id)
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
    department_id,
    manager_id
)
VALUES
    ('Gaurav', 'gaurav@example.com', 90000, TRUE, 1, NULL),
    ('Rahul', 'rahul@example.com', 70000, TRUE, 1, 1),
    ('Priya', 'priya@example.com', 65000, TRUE, 2, 1),
    ('Aman', 'aman@example.com', 50000, FALSE, 3, 1);
	
-- ----------------------------
-- Basic CTE
-- ----------------------------

WITH high_salary_employees AS (
    SELECT id, name, salary
    FROM employees
    WHERE salary > 60000
)
SELECT *
FROM high_salary_employees
ORDER BY salary DESC;

-- ----------------------------
-- CTE With Aggregation
-- ----------------------------

WITH department_summary AS (
    SELECT
        department_id,
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
)
SELECT *
FROM department_summary
WHERE average_salary > 60000;

-- ----------------------------
-- Multiple CTEs
-- ----------------------------

WITH active_employees AS (
    SELECT id, name, salary, department_id
    FROM employees
    WHERE active = TRUE
),
department_summary AS (
    SELECT
        department_id,
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary
    FROM active_employees
    GROUP BY department_id
)
SELECT *
FROM department_summary
ORDER BY average_salary DESC;

-- ----------------------------
-- CTE With INSERT
-- ----------------------------

WITH new_employee AS (
    INSERT INTO employees (
        name,
        email,
        salary,
        active,
        department_id
    )
    VALUES (
        'Neha',
        'neha@example.com',
        60000,
        TRUE,
        2
    )
    RETURNING id, name, email
)
SELECT *
FROM new_employee;

-- ----------------------------
-- CTE With UPDATE
-- ----------------------------

WITH updated_employees AS (
    UPDATE employees
    SET salary = salary * 1.10
    WHERE department_id = 1
    RETURNING id, name, salary
)
SELECT *
FROM updated_employees;

-- ----------------------------
-- CTE With DELETE
-- ----------------------------

WITH deleted_employees AS (
    DELETE FROM employees
    WHERE active = FALSE
    RETURNING id, name, email
)
SELECT *
FROM deleted_employees;

-- ----------------------------
-- Recursive CTE
-- ----------------------------

WITH RECURSIVE numbers AS (
    SELECT 1 AS number

    UNION ALL

    SELECT number + 1
    FROM numbers
    WHERE number < 5
)
SELECT number
FROM numbers;

-- ----------------------------
-- Recursive Employee Hierarchy
-- ----------------------------

WITH RECURSIVE employee_hierarchy AS (
    SELECT
        id,
        name,
        manager_id,
        1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.name,
        e.manager_id,
        h.level + 1
    FROM employees AS e
    JOIN employee_hierarchy AS h
        ON e.manager_id = h.id
)
SELECT *
FROM employee_hierarchy
ORDER BY level, id;

-- Final Data

SELECT * FROM departments;
SELECT * FROM employees;
