  -- SELECT CASE statement in SQL = It’s used for conditional logic inside a query, just like if...else in programming.

USE COMPANY;

 -- Categorize salary levels
SELECT EMPLOYEE_NAME, SALARY,
       CASE
			WHEN SALARY > 70000 THEN 'HIGH SALARY'
            WHEN SALARY BETWEEN 50000 AND 70000 THEN 'MEDIUUM SALARY'
            ELSE 'LOW SALARY'
	   END AS SALARY_CATEGORY
FROM EMPLOYEE_INFO;

  -- Age group classification
SELECT employee_name, age,
       CASE
           WHEN age > 30 THEN 'Senior'
           WHEN age BETWEEN 25 AND 30 THEN 'Mid Level'
           ELSE 'Fresher'
       END AS age_group
FROM employee_info;

  --  Bonus calculation
SELECT employee_name, designation, salary,
       CASE
           WHEN designation = 'Manager' THEN salary * 0.20
           WHEN designation = 'Developer' THEN salary * 0.15
           ELSE salary * 0.10
       END AS bonus
FROM employee_info;


SELECT *FROM EMPLOYEE_info;
