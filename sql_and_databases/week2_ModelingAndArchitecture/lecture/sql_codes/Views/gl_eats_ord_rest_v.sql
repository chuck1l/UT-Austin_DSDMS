CREATE VIEW gl_eats_ord_rest_v AS
    SELECT 
        rest.RESTAURANT_NAME,
        rest.CITY_NAME,
        rest.COUNTRY_CD,
        rest.CUISINES,
        rest.RESTAURANT_RATING,
        ord.ORDER_ID,
        ord.CUSTOMER_ID,
        ord.RESTAURANT_ID,
        ord.ORDER_COST,
        ord.ORDER_ITEMS,
        ord.DISCOUNT,
        ord.WEEK_NUMBER
    FROM gl_eats_rest_t rest
        JOIN gl_eats_ord_t ord ON 
            rest.RESTAURANT_ID = ord.RESTAURANT_ID;
