CREATE TABLE employees_hierarchy (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    manager_id INT NULL,
    department VARCHAR(50)
);

INSERT INTO employees_hierarchy VALUES
(1, 'Alice Johnson', NULL, 'Executive'),     -- CEO
(2, 'Bob Smith', 1, 'IT'),                   -- Reports to Alice
(3, 'Carol Davis', 1, 'Sales'),              -- Reports to Alice
(4, 'David Lee', 2, 'IT'),                  -- Reports to Bob
(5, 'Emma Wilson', 2, 'IT'),                -- Reports to Bob
(6, 'Frank Brown', 3, 'Sales'),             -- Reports to Carol
(7, 'Grace Kim', 3, 'Sales'),               -- Reports to Carol
(8, 'Henry Chen', 4, 'IT');                 -- Reports to David

-- Non-Recursive CTE (Simple)
-- Break down complex query - Find departments with above-average salary

with dept_avg as ( select department, avg(salary) as avg_salary from employees2 group by department) select e.emp_name, e.department, e.salary, d.avg_salary from employees2 e join dept_avg d on e.department = d.department where e.salary > d.avg_salary order by department;
+----------------+------------+----------+--------------+
| emp_name       | department | salary   | avg_salary   |
+----------------+------------+----------+--------------+
| Robert Taylor  | HR         | 58000.00 | 57800.000000 |
| Stephanie Kim  | HR         | 62000.00 | 57800.000000 |
| Daniel Park    | HR         | 62000.00 | 57800.000000 |
| James Wilson   | IT         | 90000.00 | 88500.000000 |
| David Lee      | IT         | 95000.00 | 88500.000000 |
| Kevin Brown    | IT         | 95000.00 | 88500.000000 |
| John Smith     | Sales      | 75000.00 | 74250.000000 |
| Chris Martinez | Sales      | 82000.00 | 74250.000000 |
| Amanda White   | Sales      | 82000.00 | 74250.000000 |
| Rachel Green   | Sales      | 79000.00 | 74250.000000 |
+----------------+------------+----------+--------------+
10 rows in set (0.00 sec)


-- Non-Recursive CTE (Aggregation)

-- Count employees in each department

with dept_count as (select department, count(*) as total_employees from employees_hierarchy group by department) select * from dept_count;
+------------+-----------------+
| department | total_employees |
+------------+-----------------+
| Executive  |               1 |
| IT         |               4 |
| Sales      |               3 |
+------------+-----------------+
3 rows in set (0.00 sec)



--Recursive CTE (Employee Hierarchy)
-- Display full organizational structure

WITH RECURSIVE emp_tree AS (

    -- Base case (Top-level manager)
    SELECT emp_id, emp_name, manager_id, 1 AS level
    FROM employees_hierarchy
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT e.emp_id, e.emp_name, e.manager_id, et.level + 1
    FROM employees_hierarchy e
    JOIN emp_tree et ON e.manager_id = et.emp_id
)
SELECT * FROM emp_tree;

+--------+---------------+------------+-------+
| emp_id | emp_name      | manager_id | level |
+--------+---------------+------------+-------+
|      1 | Alice Johnson |       NULL |     1 |
|      2 | Bob Smith     |          1 |     2 |
|      3 | Carol Davis   |          1 |     2 |
|      4 | David Lee     |          2 |     3 |
|      5 | Emma Wilson   |          2 |     3 |
|      6 | Frank Brown   |          3 |     3 |
|      7 | Grace Kim     |          3 |     3 |
|      8 | Henry Chen    |          4 |     4 |
+--------+---------------+------------+-------+
8 rows in set (0.00 sec)

Scheduling trip: 