-- ==================================================
-- PostgreSQL Indexes
-- Purpose: Improve query performance with appropriate indexes
-- ==================================================

DROP TABLE IF EXISTS index_employees;

CREATE TABLE index_employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    preferences JSONB NOT NULL DEFAULT '{}',
    hire_date DATE NOT NULL
);

-- Insert sample employees

INSERT INTO index_employees
    (name, email, department, salary, is_active, preferences, hire_date)
VALUES
    ('Rahul', 'rahul@example.com', 'IT', 80000, TRUE,
     '{"theme": "dark", "notifications": true}', '2024-01-15'),
    ('Priya', 'priya@example.com', 'IT', 90000, TRUE,
     '{"theme": "light", "notifications": true}', '2023-06-10'),
    ('Aman', 'aman@example.com', 'HR', 55000, FALSE,
     '{"theme": "dark", "notifications": false}', '2022-08-20'),
    ('Neha', 'neha@example.com', 'HR', 65000, TRUE,
     '{"theme": "light", "notifications": true}', '2025-01-05'),
    ('Karan', 'karan@example.com', 'Sales', 70000, TRUE,
     '{"theme": "dark", "notifications": false}', '2024-03-12'),
    ('Simran', 'simran@example.com', 'Sales', 75000, FALSE,
     '{"theme": "light", "notifications": true}', '2023-11-25');

-- 1. B-tree index: Find employees by department

CREATE INDEX idx_index_employees_department
ON index_employees (department);

SELECT *
FROM index_employees
WHERE department = 'IT';

-- 2. Composite index: Filter by department and salary

CREATE INDEX idx_index_employees_department_salary
ON index_employees (department, salary);

SELECT *
FROM index_employees
WHERE department = 'IT'
  AND salary >= 80000
ORDER BY salary DESC;

-- 3. Partial index: Index active employees only

CREATE INDEX idx_index_employees_active_department
ON index_employees (department)
WHERE is_active = TRUE;

SELECT *
FROM index_employees
WHERE department = 'IT'
  AND is_active = TRUE;

-- 4. Expression index: Case-insensitive email search

CREATE INDEX idx_index_employees_lower_email
ON index_employees (LOWER(email));

SELECT *
FROM index_employees
WHERE LOWER(email) = LOWER('RAHUL@example.com');

-- 5. GIN index: Search JSONB data

CREATE INDEX idx_index_employees_preferences
ON index_employees USING GIN (preferences);

SELECT *
FROM index_employees
WHERE preferences @> '{"theme": "dark"}';

-- 6. Unique index: Enforce unique email addresses

CREATE UNIQUE INDEX idx_index_employees_email_unique
ON index_employees (email);

-- 7. Inspect indexes on the table

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'index_employees'
ORDER BY indexname;

-- 8. Drop an index that is no longer required

DROP INDEX IF EXISTS idx_index_employees_active_department;
