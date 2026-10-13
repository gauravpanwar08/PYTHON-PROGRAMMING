-- ==================================================
-- PostgreSQL Query Performance
-- Purpose: Analyze and optimize SQL query execution
-- ==================================================

DROP TABLE IF EXISTS performance_employees;

CREATE TABLE performance_employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Insert sample data

INSERT INTO performance_employees
    (name, email, department, salary, is_active)
SELECT
    'Employee ' || n,
    'employee' || n || '@example.com',
    'Department-' || (n % 20),
    30000 + (n % 100) * 1000,
    n % 5 <> 0
FROM generate_series(1, 20000) AS n;

-- 1. Inspect the estimated execution plan

EXPLAIN
SELECT id, name, salary
FROM performance_employees
WHERE department = 'Department-7';

-- 2. Execute the query and inspect actual performance

EXPLAIN ANALYZE
SELECT id, name, salary
FROM performance_employees
WHERE department = 'Department-7';

-- 3. Include buffer information

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, name, salary
FROM performance_employees
WHERE department = 'Department-7';

-- 4. Update table statistics

ANALYZE performance_employees;

-- 5. Create an index for department filtering

CREATE INDEX idx_performance_employees_department
ON performance_employees (department);

-- 6. Refresh statistics after creating the index

ANALYZE performance_employees;

-- 7. Inspect the execution plan after indexing

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, name, salary
FROM performance_employees
WHERE department = 'Department-7';

-- 8. Inspect the plan for an equality search on email

CREATE UNIQUE INDEX idx_performance_employees_email
ON performance_employees (email);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, name, department
FROM performance_employees
WHERE email = 'employee150@example.com';

-- 9. Inspect the plan for filtering and sorting

CREATE INDEX idx_performance_employees_department_salary
ON performance_employees (department, salary DESC);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, name, salary
FROM performance_employees
WHERE department = 'Department-7'
ORDER BY salary DESC
LIMIT 10;

-- 10. Inspect indexes and their definitions

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'performance_employees'
ORDER BY indexname;

-- 11. Inspect table statistics

SELECT
    schemaname,
    tablename,
    n_live_tup,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE relname = 'performance_employees';
