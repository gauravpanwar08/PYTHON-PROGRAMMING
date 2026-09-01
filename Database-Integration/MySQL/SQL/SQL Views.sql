-- A VIEW is a virtual table that shows the result of a saved query.
-- It does not store data itself. It simplifies complex queries and can also be used for security (show only selected columns/rows).
-- VIEW → Virtual table (saved query)

USE company;

CREATE TABLE employee_info (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,  -- unique ID
    employee_name VARCHAR(100) NOT NULL,         -- naam
    designation VARCHAR(50) NOT NULL,            -- designation
    mobile BIGINT UNIQUE,                        -- mobile number unique
    age INT CHECK (age >= 18),                   -- minimum age 18
    gender ENUM('Male','Female','Other'),        -- gender fixed values
    email VARCHAR(100) UNIQUE,                   -- unique email
    salary DECIMAL(10,2) CHECK (salary >= 0),    -- salary non-negative
    joining_date DATE NOT NULL,                  -- joining date
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP, -- last login default current time
    is_active BOOLEAN DEFAULT TRUE               -- employee active/inactive
) ENGINE=InnoDB;

INSERT INTO employee_info
(employee_name, designation, mobile, age, gender, email, salary, joining_date) 
VALUES
('Anita Mehta', 'Project Manager', 9988776655, 32, 'Female', 'anita@example.com', 90000.00, '2021-06-12'),
('Rohan Kapoor', 'Web Designer', 8899001122, 25, 'Male', 'rohan@example.com', 45000.00, '2023-01-05'),
('Priya Singh', 'Database Admin', 7766554433, 29, 'Female', 'priya@example.com', 70000.00, '2022-03-18'),
('Amit Kumar', 'Network Engineer', 7001122334, 28, 'Male', 'amit@example.com', 55000.00, '2023-07-21'),
('Simran Kaur', 'HR Executive', 8800223344, 26, 'Female', 'simran@example.com', 40000.00, '2022-11-15'),
('Deepak Yadav', 'Software Tester', 9099887766, 27, 'Male', 'deepak@example.com', 48000.00, '2023-05-10'),
('Kavita Joshi', 'UI/UX Designer', 9200112233, 30, 'Female', 'kavita@example.com', 62000.00, '2021-09-25'),
('Vikas Sharma', 'Cloud Engineer', 9311223344, 31, 'Male', 'vikas@example.com', 80000.00, '2022-12-01'),
('Meena Rathi', 'Business Analyst', 9411223344, 29, 'Female', 'meena@example.com', 65000.00, '2023-03-09'),
('Harish Rawat', 'DevOps Engineer', 9511223344, 33, 'Male', 'harish@example.com', 85000.00, '2021-10-28');

SELECT * FROM employee_info;

SHOW TABLE STATUS WHERE name = 'employee_info';
DESCRIBE employee_info;
SHOW INDEX FROM employee_info;

CREATE VIEW Contact_View AS
SELECT Employee_id, Employee_Name, Mobile 
FROM employee_info;

SELECT * FROM contact_view;

CREATE VIEW Salary_View AS
SELECT employee_id, employee_name, salary 
FROM employee_info;

CREATE VIEW high_salary_employees AS
SELECT employee_name, designation, salary
FROM employee_info
WHERE salary > 60000;

DROP VIEW high_salary_employees;

SELECT * FROM Salary_View;

SELECT * FROM Salary_View
WHERE salary > 70000;

