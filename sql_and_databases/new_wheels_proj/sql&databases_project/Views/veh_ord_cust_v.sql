-- Creating a view to join the orders and customer tables
-- Utilizing functions to create calculations

CREATE VIEW veh_ord_cust_v AS 
	SELECT
		ct.CUSTOMER_ID
        , ct.CREDIT_CARD_TYPE
        , ct.STATE
        , ot.QUARTER_NUMBER
        , CUSTOMER_FEEDBACK
        , getNumericFeedback(ot.CUSTOMER_FEEDBACK) AS NUMERIC_FEEDBACK -- Function utilized to convert feedback
        , calculateRevenue(ot.VEHICLE_PRICE, ot.DISCOUNT) AS REVENUE -- Function utilized to calculate revenue, price minus discount
        , daysToShip(ot.ORDER_DATE, ot.SHIP_DATE) AS SHIPPING_TIME -- Funtion utilized to calculate the shipping time in days
        , ot.ORDER_ID
        , ot.VEHICLE_PRICE
        , ot.DISCOUNT
        , ot.ORDER_DATE
        , ot.SHIP_DATE
	FROM order_t ot
    JOIN customer_t ct
    ON ot.CUSTOMER_ID = ct.CUSTOMER_ID;