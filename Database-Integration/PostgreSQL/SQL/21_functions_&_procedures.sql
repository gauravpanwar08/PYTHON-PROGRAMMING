-- ==================================================
-- PostgreSQL Functions & Procedures
-- Purpose: Create reusable database logic
-- ==================================================


-- Clean up previous examples

DROP PROCEDURE IF EXISTS update_employee_salary(INTEGER, NUMERIC);
DROP FUNCTION IF EXISTS get_department_employees(TEXT);
DROP FUNCTION IF EXISTS salary_category(NUMERIC);
DROP FUNCTION IF EXISTS calculate_bonus(NUMERIC);
DROP FUNCTION IF EXISTS add_numbers(INTEGER, INTEGER);

DROP TABLE IF EXISTS routine_employees;

-- Create sample table

CREATE TABLE routine_employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary >= 0)
);

INSERT INTO routine_employees (name, department, salary)
VALUES
    ('Rahul', 'IT', 80000),
    ('Priya', 'HR', 65000),
    ('Aman', 'IT', 45000),
    ('Neha', 'Sales', 55000);

-- SQL function: Add two numbers

CREATE FUNCTION add_numbers(a INTEGER, b INTEGER)
RETURNS INTEGER
LANGUAGE SQL
AS $$
    SELECT a + b;
$$;

SELECT add_numbers(10, 20) AS result;

-- PL/pgSQL function: Calculate a 10% bonus

CREATE FUNCTION calculate_bonus(employee_salary NUMERIC)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN employee_salary * 0.10;
END;
$$;

SELECT
    name,
    salary,
    calculate_bonus(salary) AS bonus
FROM routine_employees;

-- Function with IF / ELSIF / ELSE

CREATE FUNCTION salary_category(employee_salary NUMERIC)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
BEGIN
    IF employee_salary >= 80000 THEN
        RETURN 'High';
    ELSIF employee_salary >= 50000 THEN
        RETURN 'Medium';
    ELSE
        RETURN 'Entry';
    END IF;
END;
$$;

SELECT
    name,
    salary,
    salary_category(salary) AS category
FROM routine_employees;

-- Function returning multiple rows

CREATE FUNCTION get_department_employees(dept TEXT)
RETURNS TABLE (
    employee_id INTEGER,
    employee_name TEXT,
    employee_salary NUMERIC
)
LANGUAGE SQL
AS $$
    SELECT
        e.id,
        e.name::TEXT,
        e.salary
    FROM routine_employees AS e
    WHERE e.department = dept;
$$;

SELECT *
FROM get_department_employees('IT');

-- Procedure: Increase an employee's salary

CREATE PROCEDURE update_employee_salary(
    employee_id INTEGER,
    increment_amount NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    affected_rows INTEGER;
BEGIN
    IF increment_amount <= 0 THEN
        RAISE EXCEPTION 'Increment must be greater than zero';
    END IF;

    UPDATE routine_employees
    SET salary = salary + increment_amount
    WHERE id = employee_id;

    GET DIAGNOSTICS affected_rows = ROW_COUNT;

    IF affected_rows = 0 THEN
        RAISE EXCEPTION 'Employee ID % not found', employee_id;
    END IF;

    RAISE NOTICE 'Salary updated for employee ID %', employee_id;
END;
$$;

CALL update_employee_salary(1, 5000);

SELECT *
FROM routine_employees
ORDER BY id;

-- Demonstrate exception handling in a function

CREATE OR REPLACE FUNCTION safe_divide(
    numerator NUMERIC,
    denominator NUMERIC
)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN numerator / denominator;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'Cannot divide by zero';
        RETURN NULL;
END;
$$;

SELECT safe_divide(100, 5) AS valid_result;
SELECT safe_divide(100, 0) AS handled_result;

-- Inspect user-defined routines

SELECT
    routine_schema,
    routine_name,
    routine_type,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name IN (
      'add_numbers',
      'calculate_bonus',
      'salary_category',
      'get_department_employees',
      'update_employee_salary',
      'safe_divide'
  )
ORDER BY routine_name;
