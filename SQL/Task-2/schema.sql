use task_1;

create table employees (
    emp_id int primary key,
    first_name varchar(50),
    last_name varchar(50),
    department varchar(50), 
    salary decimal(10, 2),
    hire_date date
)

insert into employees values 
( 101, 'Alia', 'Johnson', 'Sales', 75000.00, '2020-03-15'),
(102, 'Bob', 'Smith', 'IT', 85000.00, '2019-07-22'),
(103, 'Carol', 'Davis', 'Sales', 65000.00, '2021-01-10'),
(104, 'David', 'Brown', 'IT', 90000.00, '2018-11-05'),
(105, 'Eve', 'Wilson', 'HR', 55000.00, '2022-02-28'),
(106, 'Frank', 'Miller', 'Sales', 72000.00, '2020-09-12');


-- filter by department
select * from employees where department = 'sales';

-- Sales employees with salary > 70,000
select * from employees where department='Sales' and salary > 70000.00;

-- Employees in IT or HR departments
select * from employees where department='IT' or department='HR';

-- Sales employees with salary > 70,000 OR IT employees with salary > 85,000
select * from employees where (department='Sales' and salary > 70000.00) or (department='IT' and salary > 85000.00);

-- Sort by salary low to high
select * from employees order by salary;

-- Sort by salary high to low
select * from employees order by salary desc;

--Sort by department first, then by salary within each department
select * from employees order by department, salary desc;

-- sort by department and salary both in desc
select * from employees order by department desc, salary desc;

-- Sort by 3rd column (department) 
select first_name, last_name, department, salary from employees order by 3;

-- Sort by 3rd column (department) in desc
select first_name, last_name, department, salary from employees order by 3 desc;

-- Employees hired after 2020 with salary > 60,000, sorted by hire date
select * from employees where hire_date > '2020-01-01' and salary > 60000.00 order by hire_date;

-- Exclude HR department
select * from employees where not department = 'HR' order by department;

-- BETWEEN: Salary range
select * from employees where salary between 60000 and 80000 order by salary;

-- IN: Multiple department values
select * from employees where department in ('Sales', 'IT') order by department, last_name;