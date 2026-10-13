-- ==================================================
-- PostgreSQL Window Functions
-- Purpose: Ranking, aggregation, running totals, and row comparisons
-- ==================================================

DROP TABLE IF EXISTS window_employees;

CREATE TABLE window_employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    hire_date DATE NOT NULL
);

-- Insert sample employees

INSERT INTO window_employees (name, department, salary, hire_date)
VALUES
    ('Rahul', 'IT', 80000, '2024-01-15'),
    ('Priya', 'IT', 90000, '2023-06-10'),
    ('Aman', 'IT', 90000, '2024-03-20'),
    ('Neha', 'IT', 65000, '2025-01-05'),
    ('Karan', 'HR', 60000, '2023-08-12'),
    ('Simran', 'HR', 70000, '2024-02-18'),
    ('Rohit', 'HR', 55000, '2025-04-01'),
    ('Anjali', 'Sales', 75000, '2023-11-25'),
    ('Vikas', 'Sales', 85000, '2024-05-14'),
    ('Meera', 'Sales', 75000, '2025-02-08');

-- 1. Basic OVER(): Calculate the overall average salary

SELECT
    name,
    department,
    salary,
    ROUND(AVG(salary) OVER (), 2) AS overall_avg_salary
FROM window_employees
ORDER BY id;

-- 2. PARTITION BY: Calculate department-wise average salary

SELECT
    name,
    department,
    salary,
    ROUND(
        AVG(salary) OVER (PARTITION BY department),
        2
    ) AS department_avg_salary
FROM window_employees
ORDER BY department, salary DESC;

-- 3. ROW_NUMBER(): Assign unique row numbers

SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC, id
    ) AS row_num
FROM window_employees
ORDER BY department, row_num;

-- 4. RANK(): Assign rankings with gaps after ties

SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM window_employees
ORDER BY department, salary_rank, id;

-- 5. DENSE_RANK(): Assign rankings without gaps

SELECT
    name,
    department,
    salary,
    DENSE_RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS dense_salary_rank
FROM window_employees
ORDER BY department, dense_salary_rank, id;

-- 6. Aggregate window functions: SUM, COUNT, MIN, MAX

SELECT
    name,
    department,
    salary,
    SUM(salary) OVER (
        PARTITION BY department
    ) AS department_total_salary,
    COUNT(*) OVER (
        PARTITION BY department
    ) AS department_employee_count,
    MIN(salary) OVER (
        PARTITION BY department
    ) AS department_min_salary,
    MAX(salary) OVER (
        PARTITION BY department
    ) AS department_max_salary
FROM window_employees
ORDER BY department, id;

-- 7. Running total using an explicit window frame

SELECT
    name,
    department,
    salary,
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY salary, id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_salary_total
FROM window_employees
ORDER BY department, salary, id;

-- 8. LAG(): Compare salary with the previous employee

SELECT
    name,
    department,
    salary,
    LAG(salary, 1, 0) OVER (
        PARTITION BY department
        ORDER BY hire_date, id
    ) AS previous_salary
FROM window_employees
ORDER BY department, hire_date, id;

-- 9. LEAD(): Compare salary with the next employee

SELECT
    name,
    department,
    salary,
    LEAD(salary) OVER (
        PARTITION BY department
        ORDER BY hire_date, id
    ) AS next_salary
FROM window_employees
ORDER BY department, hire_date, id;

-- 10. Top 2 employees in each department using ROW_NUMBER()

WITH ranked_employees AS (
    SELECT
        id,
        name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC, id
        ) AS row_num
    FROM window_employees
)
SELECT
    name,
    department,
    salary,
    row_num
FROM ranked_employees
WHERE row_num <= 2
ORDER BY department, row_num;

-- 11. Top salary ranks in each department using DENSE_RANK()

WITH ranked_employees AS (
    SELECT
        name,
        department,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS salary_rank
    FROM window_employees
)
SELECT
    name,
    department,
    salary,
    salary_rank
FROM ranked_employees
WHERE salary_rank <= 2
ORDER BY department, salary_rank, name;

-- 12. Compare each salary with the department average

SELECT
    name,
    department,
    salary,
    ROUND(
        AVG(salary) OVER (PARTITION BY department),
        2
    ) AS department_avg_salary,
    ROUND(
        salary - AVG(salary) OVER (PARTITION BY department),
        2
    ) AS difference_from_average
FROM window_employees
ORDER BY department, salary DESC;
