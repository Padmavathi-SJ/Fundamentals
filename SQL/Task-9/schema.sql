CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2),
    sale_date DATE
);

INSERT INTO sales (amount, sale_date) VALUES
(1000, '2024-01-01'),
(2000, '2024-01-05'),
(1500, '2024-02-01');


-- Stored Procedure
-- A stored procedure is used to perform operations (like fetching data, updated).
-- It can accept input parameters.
-- Returns result using SELECT.

DELIMITER $$

CREATE PROCEDURE get_total_sales(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT SUM(amount) AS total_sales
    FROM sales
    WHERE sale_date BETWEEN start_date AND end_date;
END $$

DELIMITER ;


-- Call Procedure
CALL get_total_sales('2024-01-01', '2024-01-31');

total_sales
3000.00



-- Dsicount function
DELIMITER $$

CREATE FUNCTION calculate_discount(amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN amount * 0.10;
END $$

DELIMITER ;

-- Call Function
SELECT amount, calculate_discount(amount) AS discount
FROM sales;

amount| discount
1000.00	100.00
2000.00	200.00
1500.00	150.00


