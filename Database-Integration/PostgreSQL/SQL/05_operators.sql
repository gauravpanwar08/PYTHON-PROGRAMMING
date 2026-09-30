-- Create employees table
ALTER TABLE employees ADD COLUMN skills TEXT[];

-- Insert sample data
INSERT INTO employees (name, salary, department, is_active, skills)
VALUES
    ('Rahul', 50000, 'Backend', TRUE, ARRAY['Python', 'SQL']),
    ('Aman', 65000, 'Frontend', TRUE, ARRAY['JavaScript', 'React']),
    ('Priya', 70000, 'Backend', TRUE, ARRAY['Python', 'FastAPI']),
    ('Neha', 45000, 'HR', FALSE, ARRAY['Excel', 'Communication']),
    ('Ankit', 80000, 'Backend', TRUE, ARRAY['Python', 'PostgreSQL']),
    ('Riya', 55000, 'HR', TRUE, ARRAY['Excel', 'SQL']);

-- Arithmetic operators
SELECT 10 + 5 AS addition;
SELECT 10 - 5 AS subtraction;
SELECT 10 * 5 AS multiplication;
SELECT 10 / 5 AS division;
SELECT 10 % 3 AS remainder;
SELECT 2 ^ 3 AS exponentiation;

-- Arithmetic with columns
SELECT
    name,
    salary,
    salary + 5000 AS increased_salary
FROM employees;

-- Comparison operator
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
OR department = 'HR';

-- NOT
SELECT *
FROM employees
WHERE NOT is_active;

-- String concatenation
SELECT
    name || ' - ' || department AS employee_info
FROM employees;

-- IN
SELECT *
FROM employees
WHERE department IN ('Backend', 'HR');

-- NOT IN
SELECT *
FROM employees
WHERE department NOT IN ('HR');

-- ANY with an array
SELECT *
FROM employees
WHERE salary > ANY (ARRAY[50000, 70000]);

-- ALL with an array
SELECT *
FROM employees
WHERE salary > ALL (ARRAY[50000, 60000]);

-- NULL-safe comparison
SELECT
    NULL IS DISTINCT FROM NULL AS different_values;

SELECT
    NULL IS NOT DISTINCT FROM NULL AS same_values;

-- Array with ANY
SELECT *
FROM employees
WHERE 'Python' = ANY(skills);

-- Array concatenation
SELECT ARRAY['Python', 'SQL'] || ARRAY['FastAPI'] AS combined_skills;

-- Combined conditions with parentheses
SELECT *
FROM employees
WHERE salary > 50000
AND (department = 'Backend' OR department = 'HR');