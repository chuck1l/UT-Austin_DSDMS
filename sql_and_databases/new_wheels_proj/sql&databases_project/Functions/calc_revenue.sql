-- This function calculates the revenue for each transaction
-- Arguments are price and discount (in percentage)
-- Returns the order revenue

DELIMITER $$
CREATE FUNCTION calculateRevenue(price DECIMAL(10,2), discount DECIMAL(4,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
	DECLARE REVENUE DECIMAL(10,2);
	SET REVENUE = price - (price * (discount/100));
    RETURN(REVENUE);
END;