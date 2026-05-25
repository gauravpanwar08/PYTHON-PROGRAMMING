-- An INDEX is a data structure (like a shortcut) that improves the speed of searching and retrieving data from a table.
-- INDEX → Improves search speed

USE COMPANY;

SHOW INDEX FROM employee_info;

SELECT * FROM employee_info;
SELECT employee_name FROM employee_info;

SELECT * FROM employee_info
WHERE employee_name='Amit Kumar' AND salary > 50000;


  -- Normal Index (only for speed up queries)
CREATE INDEX idx_name ON employee_info(employee_name);

DROP INDEX idx_name ON employee_info;

  -- Composite Index (multi-column index)
CREATE INDEX idx_name_salary 
ON employee_info(employee_name, salary);

DROP INDEX idx_name_salary ON employee_info;

  -- Full-Text Index (fast from LIKE operator)
CREATE FULLTEXT INDEX idx_emp_name_full 
ON employee_info(employee_name);

SELECT * FROM employee_info
WHERE MATCH(employee_name) AGAINST('Deepak Yadav');

DROP INDEX idx_emp_name_full ON employee_info;


