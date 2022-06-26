-- Creating a view to join the products to customer tables

CREATE VIEW veh_prod_cust_v AS 
	SELECT
		ct.CUSTOMER_ID
        , ct.STATE
        , ot.ORDER_ID
        , pt.VEHICLE_MAKER
	FROM order_t ot -- Multiple joins necessary to get all information 
    LEFT JOIN product_t pt
		ON ot.PRODUCT_ID = pt.PRODUCT_ID
    LEFT JOIN customer_t ct
		ON ot.CUSTOMER_ID = ct.CUSTOMER_ID
