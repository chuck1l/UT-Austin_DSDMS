CREATE VIEW gl_eats_del_rest_v AS
    SELECT 
        rest.RESTAURANT_ID,
        rest.RESTAURANT_NAME,
        rest.CITY_NAME,
        rest.COUNTRY_CD,
        rest.RESTAURANT_RATING,
        del.DELIVERY_ID,
        del.DELIVERY_EMP_ID,
        del.ORDER_ID,
        del.DELIVERY_STATUS,
        del.STAR_RATING,
        del.WEEK_NUMBER
    FROM gl_eats_rest_t rest
        JOIN gl_eats_del_t del 
            ON rest.RESTAURANT_ID = del.RESTAURANT_ID;
