CREATE VIEW gl_eats_ord_dubai_v AS (
SELECT ord.*, rest.CITY_NAME 
FROM gl_eats_ord_t ord 
	INNER JOIN  (SELECT DISTINCT 
			RESTAURANT_ID, 
			CITY_NAME 
		     FROM gl_eats_rest_t
		     WHERE CITY_NAME = 'Dubai') rest
	ON ord.RESTAURANT_ID = rest.RESTAURANT_ID
);
