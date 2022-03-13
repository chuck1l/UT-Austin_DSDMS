DELIMITER $$
CREATE PROCEDURE gl_eats_rest_p()
BEGIN
    INSERT INTO gl_eats_rest_t (
        RESTAURANT_ID, 
        RESTAURANT_NAME, 
        CITY_NAME, 
        COUNTRY_CD,
        ADDRESS, 
        LOCALITY, 
        LONGITUDE, 
        LATITUDE, 
        CUISINES, 
        RESTAURANT_RATING
	) 
    SELECT DISTINCT 
	RESTAURANT_ID, 
        RESTAURANT_NAME, 
        CITY_NAME, 
        COUNTRY_CD,
        ADDRESS, 
        LOCALITY, 
        LONGITUDE, 
        LATITUDE, 
        CUISINES, 
        RESTAURANT_RATING
	FROM gl_eats_t WHERE RESTAURANT_ID NOT IN (SELECT DISTINCT RESTAURANT_ID FROM gl_eats_rest_t);
END;

-- CALL gl_eats_rest_p();
