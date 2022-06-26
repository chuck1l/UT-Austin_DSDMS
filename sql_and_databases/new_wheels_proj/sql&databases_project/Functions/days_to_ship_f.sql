-- This function calculates the days it took to ship a vehicle
-- Arguments are the order date and the shipping date
-- Returns the difference of those two dates, in days

DELIMITER $$
CREATE FUNCTION daysToShip(order_date DATE, ship_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE SHIPPING_TIME INT;
	SET SHIPPING_TIME = DATEDIFF(ship_date, order_date);
    RETURN(SHIPPING_TIME);
END;