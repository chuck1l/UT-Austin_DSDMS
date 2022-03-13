DELIMITER $$
CREATE PROCEDURE gl_eats_ord_p(weeknum INTEGER)
BEGIN
	INSERT INTO gl_eats_ord_t (
	ORDER_ID, 
        DELIVERY_EMP_ID, 
        CUSTOMER_ID, 
        RESTAURANT_ID,
        ORDER_COST, 
        ORDER_ITEMS, 
        DISCOUNT, 
        WEEK_NUMBER
	) 
    SELECT DISTINCT
	ORDER_ID, 
        DELIVERY_EMP_ID, 
        CUSTOMER_ID, 
        RESTAURANT_ID ,
        ORDER_COST, 
        ORDER_ITEMS, 
        DISCOUNT, 
        WEEK_NUMBER
	FROM gl_eats_t WHERE WEEK_NUMBER = weeknum;
END;

-- CALL gl_eats_ord_p(1);
