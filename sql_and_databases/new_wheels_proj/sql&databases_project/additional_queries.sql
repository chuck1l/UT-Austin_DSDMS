SELECT AVG(SHIPPING_TIME)
FROM veh_ord_cust_v;

SELECT COUNT(DISTINCT customer_id)
FROM veh_ord_cust_v;

SELECT COUNT(DISTINCT order_id)
FROM veh_ord_cust_v;

SELECT COUNT(DISTINCT order_id)
FROM veh_ord_cust_v
WHERE quarter_number = 4;