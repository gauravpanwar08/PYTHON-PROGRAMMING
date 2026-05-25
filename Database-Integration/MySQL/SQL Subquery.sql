-- A Subquery (or inner/nested query) is a query inside another SQL query.
-- The inner query runs first, and its result is used by the outer query.

USE COMPANY;
SHOW TABLES;

 -- 1. Single-row Subquery - Returns only one value (one row, one column).
SELECT EMPLOYEE_NAME, SALARY
FROM EMPLOYEE_INFO
WHERE SALARY = (SELECT MAX(SALARY) FROM EMPLOYEE_INFO);

 -- 2. Multi-row Subquery - Returns multiple rows. Use operators like IN, ANY, ALL.
 SELECT EMPLOYEE_NAME, DESIGNATION
 FROM EMPLOYEE_INFO
 WHERE SALARY IN (SELECT SALARY FROM EMPLOYEE_INFO WHERE DESIGNATION = 'DATABASE ADMIN');
 
 SELECT AVG(SALARY) FROM EMPLOYEE_INFO;
 
 SELECT EMPLOYEE_NAME, SALARY
 FROM EMPLOYEE_INFO
 WHERE SALARY > (SELECT AVG(SALARY) FROM EMPLOYEE_INFO);
 
   -- 3. Multi-column Subquery - Returns multiple columns.
SELECT EMPLOYEE_NAME, SALARY
FROM EMPLOYEE_INFO
WHERE (GENDER, SALARY) IN (SELECT GENDER, SALARY FROM EMPLOYEE_INFO WHERE GENDER = 'FEMALE');

  -- 4. Correlated Subquery - The subquery depends on the outer query & Runs once for every row of the outer query.
SELECT e1.employee_name, e1.salary
FROM employee_info e1
WHERE salary = (SELECT AVG(e2.salary) 
                FROM employee_info e2 
                WHERE e1.designation = e2.designation);
                
  -- 5. Subquery in FROM clause (Inline View) - we can use a subquery like a temporary table.
SELECT designation, AVG(salary) AS avg_salary
FROM (SELECT * FROM employee_info WHERE age > 25) AS temp
GROUP BY designation;

  -- 6. Subquery with INSERT - we can use a subquery to fetch/copy data from another table and insert it into the target table.
CREATE TABLE employee_backup (
    employee_id INT,
    employee_name VARCHAR(50),
    designation VARCHAR(50),
    salary DECIMAL(10,2)
);
INSERT INTO employee_backup (employee_id, employee_name, designation, salary)
SELECT employee_id, employee_name, designation, salary
FROM employee_info
WHERE salary > 50000;

  -- 7. Subquery with UPDATE - We can update rows in one table using data from another table (or the same table).
UPDATE employee_info
SET salary = salary / 1.10
WHERE dept_id = (
    SELECT dept_id FROM departments WHERE dept_name = 'IT'
);

  -- 8. Subquery with DELETE - We can delete rows based on conditions from another table.
DELETE FROM employee_info
WHERE dept_id NOT IN (
    SELECT dept_id FROM departments
);
ALTER TABLE employee_info
ADD dept_id INT,
ADD CONSTRAINT fk_dept
FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

DESC employee_info;          -- table details
SET SQL_SAFE_UPDATES = 0;    -- safe mode off
SET SQL_SAFE_UPDATES = 1;    -- safe mode on
SELECT *FROM EMPLOYEE_info;
 