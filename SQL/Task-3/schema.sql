-- going to use the same employees table

SELECT COUNT(*) AS total_employees FROM Employees;

SELECT SUM(salary) AS total_salary FROM Employees;

SELECT AVG(salary) AS average_salary FROM Employees;

SELECT MIN(salary) AS lowest_salary, 
       MAX(salary) AS highest_salary 
FROM Employees;

SELECT department, 
       COUNT(*) AS employee_count
FROM Employees
GROUP BY department;

SELECT department, 
       COUNT(*) AS num_employees,
       SUM(salary) AS total_salary,
       AVG(salary) AS avg_salary,
       MIN(salary) AS min_salary,
       MAX(salary) AS max_salary
FROM Employees
GROUP BY department;


SELECT department, COUNT(*) AS employee_count
FROM Employees
GROUP BY department
HAVING COUNT(*) > 2;


SELECT department, AVG(salary) AS avg_salary
FROM Employees
GROUP BY department
HAVING AVG(salary) > 70000;


SELECT department, 
       COUNT(*) AS emp_count,
       AVG(salary) AS avg_salary
FROM Employees
WHERE hire_date > '2019-01-01'  
GROUP BY department
HAVING AVG(salary) > 65000
ORDER BY avg_salary DESC;