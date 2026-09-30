-- Create sample table
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    department VARCHAR(50),
    salary NUMERIC(10, 2),
    phone VARCHAR(20),
    joining_date DATE
);

-- Insert sample data
INSERT INTO employees
(name, email, department, salary, phone, joining_date)
VALUES
('Gaurav Panwar', 'gaurav@example.com', 'Backend', 85000.50, '9876543210', '2025-07-15'),
('Rahul Sharma', 'rahul@example.com', 'Frontend', 62000.75, NULL, '2024-03-10'),
('Ankit Verma', 'ankit@example.com', 'Backend', 48000.25, '9123456780', '2023-11-20'),
('Priya Singh', 'priya@example.com', 'Data', 92000.00, NULL, '2022-08-05');

-- ------------------
-- String Functions
-- ------------------

SELECT LOWER(name) AS lowercase_name
FROM employees;

SELECT UPPER(name) AS uppercase_name
FROM employees;

SELECT LENGTH(name) AS name_length
FROM employees;

SELECT TRIM('  PostgreSQL   ') AS trimmed_text;

SELECT SUBSTRING(name FROM 1 FOR 6) AS short_name
FROM employees;

SELECT REPLACE(department, 'Backend', 'Python Backend') AS updated_department
FROM employees;

SELECT CONCAT(name, ' - ', department) AS employee_info
FROM employees;

SELECT CONCAT_WS(' | ', name, department, salary) AS employee_details
FROM employees;

-- ------------------
-- Numeric Functions
-- ------------------

SELECT ROUND(salary, 0) AS rounded_salary
FROM employees;

SELECT CEIL(salary) AS ceiling_salary
FROM employees;

SELECT FLOOR(salary) AS floor_salary
FROM employees;

SELECT ABS(-500) AS absolute_value;

SELECT MOD(10, 3) AS remainder;

SELECT POWER(2, 3) AS power_result;

SELECT RANDOM() AS random_value;

-- ------------------
-- Date and Time Functions
-- ------------------

SELECT CURRENT_DATE AS current_date;

SELECT CURRENT_TIME AS current_time;

SELECT CURRENT_TIMESTAMP AS current_timestamp;

SELECT NOW() AS current_timestamp;

SELECT EXTRACT(YEAR FROM joining_date) AS joining_year
FROM employees;

SELECT EXTRACT(MONTH FROM joining_date) AS joining_month
FROM employees;

SELECT DATE_TRUNC('month', CURRENT_TIMESTAMP) AS month_start;

SELECT DATE_TRUNC('day', CURRENT_TIMESTAMP) AS day_start;

SELECT AGE(CURRENT_DATE, joining_date) AS experience_period
FROM employees;

-- ------------------
-- CASE
-- ------------------

SELECT name, salary,
    CASE
        WHEN salary >= 80000 THEN 'High'
        WHEN salary >= 50000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_level
FROM employees;

-- ------------------
-- COALESCE
-- ------------------

SELECT
    name,
    COALESCE(phone, 'Not Provided') AS phone
FROM employees;

-- ------------------
-- NULLIF
-- ------------------

SELECT NULLIF(10, 10) AS same_values;

SELECT NULLIF(10, 20) AS different_values;

-- ------------------
-- Type Conversion
-- ------------------

SELECT CAST('100' AS INTEGER) AS converted_number;

SELECT '100'::INTEGER AS converted_number;

SELECT
    name,
    salary::INTEGER AS integer_salary
FROM employees;

