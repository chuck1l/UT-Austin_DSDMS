-- DROP FUNCTION calcRevenue;

DELIMITER $$  
CREATE FUNCTION calcRevenue(order_cost INT, discount INT, delivery_status INT)  
RETURNS INT  
DETERMINISTIC  
BEGIN  
    DECLARE revenue INT;
    IF delivery_status = 4 THEN  
        SET revenue = 0;  
    ELSEIF delivery_status = 1 OR delivery_status = 2 OR delivery_status = 3 THEN  
        SET revenue = order_cost - discount;  
    END IF;  
    RETURN (revenue);  
END;

-- SELECT 
--     ORDER_ID, 
--     ORDER_COST, 
--     DISCOUNT, 
--     DELIVERY_STATUS, 
-- 	calcRevenue(ORDER_COST, DISCOUNT, DELIVERY_STATUS) REVENUE 
-- FROM gl_eats_del_ord_v;

-- SELECT
--     WEEK_NUMBER,
--     SUM(calcRevenue(ORDER_COST, DISCOUNT, DELIVERY_STATUS)) REVENUE
-- FROM gl_eats_del_ord_v
-- GROUP BY 1;
