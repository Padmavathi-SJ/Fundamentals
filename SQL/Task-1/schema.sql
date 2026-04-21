create database if not exists task_1

create table products (
    product_id int primary key,
    product_name varchar(50) not null,
    price decimal(10, 2),
    quantity_in_stocks int default 0
)

INSERT INTO Products (product_id, product_name, price, quantity_in_stocks) VALUES
(1, 'Laptop', 899.99, 10),
(2, 'Mouse', 24.50, 50),
(3, 'Keyboard', 45.99, 30);


select * from products;

select * from products where price=24.50