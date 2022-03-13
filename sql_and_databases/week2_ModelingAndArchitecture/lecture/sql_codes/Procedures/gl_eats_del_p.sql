DELIMITER $$
CREATE PROCEDURE gl_eats_del_p(weeknum INTEGER)
BEGIN
	INSERT INTO gl_eats_del_t (
	DELIVERY_ID,
	DELIVERY_EMP_ID, 
        ORDER_ID, 
        DELIVERY_STATUS, 
        RESTAURANT_ID, 
        STAR_RATING,
        WEEK_NUMBER
	) 
    SELECT DISTINCT
	DELIVERY_ID,
	DELIVERY_EMP_ID, 
        ORDER_ID, 
        DELIVERY_STATUS, 
        RESTAURANT_ID, 
        STAR_RATING,
        WEEK_NUMBER
	FROM gl_eats_t WHERE WEEK_NUMBER = weeknum;
END;

-- CALL gl_eats_del_p(1);
