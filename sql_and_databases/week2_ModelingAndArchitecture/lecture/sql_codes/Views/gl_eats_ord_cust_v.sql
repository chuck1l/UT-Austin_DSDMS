CREATE VIEW gl_eats_cust_ord_v AS
    SELECT 
        cust.CUSTOMER_ID,
        cust.CUSTOMER_NAME,
        cust.COUNTRY_CD,
        ord.ORDER_ID,
        ord.RESTAURANT_ID,
        ord.ORDER_COST,
        ord.ORDER_ITEMS,
        ord.DISCOUNT,
        ord.WEEK_NUMBER
    FROM gl_eats_cust_t cust
        JOIN gl_eats_ord_t ord ON 
            cust.CUSTOMER_ID = ord.CUSTOMER_ID;
