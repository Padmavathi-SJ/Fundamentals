
-- ROW_NUMBER() - Unique Sequential Ranking
-- Assign a unique sequential number to each employee within their department based on salary (highest to lowest)

select emp_name, department, salary, row_number() over (partition by department order by salary desc) as rank_in_dept from employees2 order by department, salary desc;
+----------------+------------+----------+--------------+
| emp_name       | department | salary   | rank_in_dept |
+----------------+------------+----------+--------------+
| Stephanie Kim  | HR         | 62000.00 |            1 |
| Daniel Park    | HR         | 62000.00 |            2 |
| Robert Taylor  | HR         | 58000.00 |            3 |
| Lisa Anderson  | HR         | 55000.00 |            4 |
| Tom Wilson     | HR         | 52000.00 |            5 |
| David Lee      | IT         | 95000.00 |            1 |
| Kevin Brown    | IT         | 95000.00 |            2 |
| James Wilson   | IT         | 90000.00 |            3 |
| Jennifer Chen  | IT         | 88000.00 |            4 |
| Emma Davis     | IT         | 85000.00 |            5 |
| Michelle Lee   | IT         | 78000.00 |            6 |
| Chris Martinez | Sales      | 82000.00 |            1 |
| Amanda White   | Sales      | 82000.00 |            2 |
| Rachel Green   | Sales      | 79000.00 |            3 |
| John Smith     | Sales      | 75000.00 |            4 |
| Mike Brown     | Sales      | 72000.00 |            5 |
| Patricia Brown | Sales      | 71000.00 |            6 |
| Maria Garcia   | Sales      | 68000.00 |            7 |
| Sarah Johnson  | Sales      | 65000.00 |            8 |
+----------------+------------+----------+--------------+
19 rows in set (0.02 sec)


-- LAG() - Previous Row Value
-- Compare each employee's salary with the previous employee in the same department
SELECT emp_name, department, salary,
       LAG(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS prev_salary,
       LAG(emp_name) OVER (PARTITION BY department ORDER BY salary DESC) AS prev_employee,
       salary - LAG(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS salary_diff_from_prev
FROM employees2
ORDER BY department, salary DESC;
+----------------+------------+----------+-------------+----------------+-----------------------+
| emp_name       | department | salary   | prev_salary | prev_employee  | salary_diff_from_prev |
+----------------+------------+----------+-------------+----------------+-----------------------+
| Stephanie Kim  | HR         | 62000.00 |        NULL | NULL           |                  NULL |
| Daniel Park    | HR         | 62000.00 |    62000.00 | Stephanie Kim  |                  0.00 |
| Robert Taylor  | HR         | 58000.00 |    62000.00 | Daniel Park    |              -4000.00 |
| Lisa Anderson  | HR         | 55000.00 |    58000.00 | Robert Taylor  |              -3000.00 |
| Tom Wilson     | HR         | 52000.00 |    55000.00 | Lisa Anderson  |              -3000.00 |
| David Lee      | IT         | 95000.00 |        NULL | NULL           |                  NULL |
| Kevin Brown    | IT         | 95000.00 |    95000.00 | David Lee      |                  0.00 |
| James Wilson   | IT         | 90000.00 |    95000.00 | Kevin Brown    |              -5000.00 |
| Jennifer Chen  | IT         | 88000.00 |    90000.00 | James Wilson   |              -2000.00 |


-- LEAD() - Next Row Value
-- Compare each employee's salary with the next employee in the same department
    -> ORDER BY department, salary DESC;
+----------------+------------+----------+-------------+----------------+---------------------+
| emp_name       | department | salary   | next_salary | next_employee  | salary_diff_to_next |
+----------------+------------+----------+-------------+----------------+---------------------+
| Stephanie Kim  | HR         | 62000.00 |    62000.00 | Daniel Park    |                0.00 |
| Daniel Park    | HR         | 62000.00 |    58000.00 | Robert Taylor  |            -4000.00 |
| Robert Taylor  | HR         | 58000.00 |    55000.00 | Lisa Anderson  |            -3000.00 |
| Lisa Anderson  | HR         | 55000.00 |    52000.00 | Tom Wilson     |            -3000.00 |
| Tom Wilson     | HR         | 52000.00 |        NULL | NULL           |                NULL |
| David Lee      | IT         | 95000.00 |    95000.00 | Kevin Brown    |                0.00 |
| Kevin Brown    | IT         | 95000.00 |    90000.00 | James Wilson   |            -5000.00 |
| James Wilson   | IT         | 90000.00 |    88000.00 | Jennifer Chen  |            -2000.00 |


-- Top Performer per Department
-- Find the top 2 highest paid employees in each department
SELECT * FROM (
    SELECT emp_name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees2
) AS ranked
WHERE rn <= 2
ORDER BY department, salary DESC;

+----------------+------------+----------+----+
| emp_name       | department | salary   | rn |
+----------------+------------+----------+----+
| Stephanie Kim  | HR         | 62000.00 |  1 |
| Daniel Park    | HR         | 62000.00 |  2 |
| David Lee      | IT         | 95000.00 |  1 |
| Kevin Brown    | IT         | 95000.00 |  2 |
| Chris Martinez | Sales      | 82000.00 |  1 |
| Amanda White   | Sales      | 82000.00 |  2 |
+----------------+------------+----------+----+
6 rows in set (0.01 sec)