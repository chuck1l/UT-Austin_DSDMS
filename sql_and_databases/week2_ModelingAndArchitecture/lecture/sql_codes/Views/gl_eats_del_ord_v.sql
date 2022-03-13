CREATE VIEW gl_eats_del_ord_v AS
    SELECT 
        ord.ORDER_ID,
        ord.CUSTOMER_ID,
        ord.RESTAURANT_ID,
        ord.DELIVERY_EMP_ID,
        ord.ORDER_COST,
        ord.DISCOUNT,
        ord.WEEK_NUMBER,
        del.DELIVERY_ID,
        del.DELIVERY_STATUS,
        del.STAR_RATING
    FROM gl_eats_ord_t ord 
        INNER JOIN gl_eats_del_t del 
            ON ord.ORDER_ID = del.ORDER_ID;
