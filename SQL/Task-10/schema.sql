CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE OrderDetails (
    order_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);


INSERT INTO Customers (name, email)
VALUES ('Padma', 'padma@gmail.com'),
       ('John', 'john@gmail.com');

INSERT INTO Products (name, price, stock)
VALUES ('Laptop', 50000, 10),
       ('Mouse', 500, 50);

INSERT INTO Orders (customer_id, order_date)
VALUES (1, '2026-04-20');

INSERT INTO OrderDetails (order_id, product_id, quantity)
VALUES (1, 1, 1),
       (1, 2, 2);



-- INDEXING (performance Optimization)
-- Used to speed up search queries
CREATE INDEX idx_customer_email ON Customers(email);
CREATE INDEX idx_product_name ON Products(name);


-- TRIGGERS (Automation)
--> ex: reduce stock after order

DELIMITER //

CREATE TRIGGER reduce_stock
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Products
    SET stock = stock - NEW.quantity
    WHERE product_id = NEW.product_id;
END //

DELIMITER ;

--> it automatically updates inventory


--> TRANSACTIONS (Data Consistency)
-> ex: order processing

START TRANSACTION;

INSERT INTO Orders (customer_id, order_date)
VALUES (1, CURDATE());

INSERT INTO OrderDetails (order_id, product_id, quantity)
VALUES (LAST_INSERT_ID(), 1, 1);

COMMIT;

-- If error:
ROLLBACK;

-- All steps succeed or none applied.


-- VIEWS
CREATE VIEW OrderSummary AS
SELECT o.order_id, c.name, p.name AS product, od.quantity
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderDetails od ON o.order_id = od.order_id
JOIN Products p ON od.product_id = p.product_id;

SELECT * FROM OrderSummary;

order_id  name    product   quantity
2	      Padma	  Laptop	  1
1	      Padma	  Laptop	  1
1	      Padma	  Mouse	      2