-- Create sample table
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary NUMERIC(10, 2),
    active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO employees
(name, department, salary, active)
VALUES
('Gaurav Panwar', 'Backend', 85000, TRUE),
('Rahul Sharma', 'Backend', 65000, TRUE),
('Ankit Verma', 'Backend', 48000, FALSE),
('Priya Singh', 'Frontend', 72000, TRUE),
('Neha Gupta', 'Frontend', 58000, TRUE),
('Aman Kumar', 'Frontend', 45000, FALSE),
('Riya Mehta', 'Data', 90000, TRUE),
('Karan Singh', 'Data', 70000, TRUE),
('Vikas Jain', 'Data', 55000, FALSE);

-- ------------------
-- COUNT
-- ------------------

SELECT COUNT(*) AS total_employees
FROM employees;

SELECT COUNT(salary) AS employees_with_salary
FROM employees;

SELECT COUNT(DISTINCT department) AS total_departments
FROM employees;

-- ------------------
-- SUM
-- ------------------

SELECT SUM(salary) AS total_salary
FROM employees;

-- ------------------
-- AVG
-- ------------------

SELECT AVG(salary) AS average_salary
FROM employees;

-- ------------------
-- MIN and MAX
-- ------------------

SELECT MIN(salary) AS minimum_salary
FROM employees;

SELECT MAX(salary) AS maximum_salary
FROM employees;

-- ------------------
-- Multiple Aggregate Functions
-- ------------------

SELECT
    COUNT(*) AS employee_count,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees;

-- ------------------
-- GROUP BY
-- ------------------

SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department;

SELECT
    department,
    SUM(salary) AS total_salary
FROM employees
GROUP BY department;

SELECT
    department,
    AVG(salary) AS average_salary
FROM employees
GROUP BY department;

-- ------------------
-- Multiple Aggregates with GROUP BY
-- ------------------

SELECT
    department,
    COUNT(*) AS employee_count,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees
GROUP BY department;

-- ------------------
-- WHERE with GROUP BY
-- ------------------

SELECT
    department,
    COUNT(*) AS active_employees,
    AVG(salary) AS average_salary
FROM employees
WHERE active = TRUE
GROUP BY department;

-- ------------------
-- HAVING
-- ------------------

SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000;

-- ------------------
-- WHERE + GROUP BY + HAVING
-- ------------------

SELECT
    department,
    COUNT(*) AS active_employees,
    AVG(salary) AS average_salary
FROM employees
WHERE active = TRUE
GROUP BY department
HAVING AVG(salary) > 60000;

-- ------------------
-- GROUP BY Multiple Columns
-- ------------------

SELECT
    department,
    active,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department, active;

-- ------------------
-- ORDER BY Aggregated Result
-- ------------------

SELECT
    department,
    SUM(salary) AS total_salary
FROM employees
GROUP BY department
ORDER BY total_salary DESC;

-- ------------------
-- COALESCE with Aggregate
-- ------------------

SELECT COALESCE(SUM(salary), 0) AS total_salary
FROM employees;

