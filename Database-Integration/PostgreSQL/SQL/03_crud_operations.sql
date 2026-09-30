-- Create employees table
CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email TEXT UNIQUE NOT NULL,
    salary NUMERIC(10, 2),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert one employee
INSERT INTO employees (name, email, salary)
VALUES ('Rahul', 'rahul@example.com', 50000);

-- Insert multiple employees
INSERT INTO employees (name, email, salary)
VALUES
    ('Aman', 'aman@example.com', 60000),
    ('Priya', 'priya@example.com', 55000),
    ('Neha', 'neha@example.com', 65000);

-- Insert and return the created row
INSERT INTO employees (name, email, salary)
VALUES ('Arjun', 'arjun@example.com', 70000)
RETURNING id, name, email, salary;

-- Select all employees
SELECT *
FROM employees;

-- Select specific columns
SELECT id, name, salary
FROM employees;

-- Select active employees
SELECT id, name, salary
FROM employees
WHERE is_active = TRUE;

-- Update employee salary
UPDATE employees
SET salary = 75000
WHERE id = 1;

-- Update and return the updated row
UPDATE employees
SET salary = 80000
WHERE id = 2
RETURNING id, name, salary;

-- Update multiple columns
UPDATE employees
SET
    salary = 70000,
    is_active = FALSE
WHERE id = 3
RETURNING id, name, salary, is_active;

-- Delete an employee
DELETE FROM employees
WHERE id = 4;

-- Delete and return the deleted row
DELETE FROM employees
WHERE id = 5
RETURNING id, name, email;

-- View final data
SELECT *
FROM employees;

