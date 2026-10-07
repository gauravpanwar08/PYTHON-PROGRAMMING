-- Create employees table
DROP TABLE IF EXISTS contractors;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    department VARCHAR(50)
);

-- Create contractors table
CREATE TABLE contractors (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    department VARCHAR(50)
);

-- Insert employees
INSERT INTO employees
(name, email, department)
VALUES
('Gaurav Panwar', 'gaurav@example.com', 'Backend'),
('Rahul Sharma', 'rahul@example.com', 'Frontend'),
('Aman Kumar', 'aman@example.com', 'Data'),
('Neha Gupta', 'neha@example.com', 'Backend');

-- Insert contractors
INSERT INTO contractors
(name, email, department)
VALUES
('Rahul Sharma', 'rahul@example.com', 'Frontend'),
('Priya Singh', 'priya@example.com', 'Data'),
('Aman Kumar', 'aman@example.com', 'Data'),
('Karan Mehta', 'karan@example.com', 'DevOps');

-- ------------------
-- UNION
-- ------------------

SELECT name
FROM employees

UNION

SELECT name
FROM contractors;

-- ------------------
-- UNION ALL
-- ------------------

SELECT name
FROM employees

UNION ALL

SELECT name
FROM contractors;

-- ------------------
-- UNION with Multiple Columns
-- ------------------

SELECT name, email
FROM employees

UNION

SELECT name, email
FROM contractors;

-- ------------------
-- INTERSECT
-- ------------------

SELECT name
FROM employees

INTERSECT

SELECT name
FROM contractors;

-- ------------------
-- EXCEPT
-- ------------------

SELECT name
FROM employees

EXCEPT

SELECT name
FROM contractors;

-- ------------------
-- Reverse EXCEPT
-- ------------------

SELECT name
FROM contractors

EXCEPT

SELECT name
FROM employees;

-- ------------------
-- UNION with ORDER BY
-- ------------------

SELECT name
FROM employees

UNION

SELECT name
FROM contractors

ORDER BY name;

-- ------------------
-- UNION ALL with ORDER BY
-- ------------------

SELECT name
FROM employees

UNION ALL

SELECT name
FROM contractors

ORDER BY name DESC;

-- ------------------
-- UNION with LIMIT
-- ------------------

SELECT name
FROM employees

UNION

SELECT name
FROM contractors

ORDER BY name

LIMIT 5;

-- ------------------
-- Individual LIMIT before UNION ALL
-- ------------------

(
    SELECT name
    FROM employees
    ORDER BY name
    LIMIT 3
)

UNION ALL

(
    SELECT name
    FROM contractors
    ORDER BY name
    LIMIT 3
);

-- ------------------
-- UNION with WHERE
-- ------------------

SELECT name
FROM employees
WHERE department = 'Backend'

UNION

SELECT name
FROM contractors
WHERE department = 'Backend';

-- ------------------
-- INTERSECT with WHERE
-- ------------------

SELECT name
FROM employees
WHERE department = 'Data'

INTERSECT

SELECT name
FROM contractors
WHERE department = 'Data';

-- ------------------
-- EXCEPT with WHERE
-- ------------------

SELECT name
FROM employees
WHERE department = 'Backend'

EXCEPT

SELECT name
FROM contractors
WHERE department = 'Backend';