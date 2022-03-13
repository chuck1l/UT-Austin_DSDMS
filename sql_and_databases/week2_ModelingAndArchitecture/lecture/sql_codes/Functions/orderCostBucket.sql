-- DROP FUNCTION orderCostBucket;

DELIMITER $$  
CREATE FUNCTION orderCostBucket(order_cost INT)  
RETURNS VARCHAR(20)  
DETERMINISTIC  
BEGIN  
    DECLARE cost_bucket VARCHAR(20);  
    IF order_cost <= 70 THEN  
        SET cost_bucket = 'Low';  
    ELSEIF (order_cost > 70 AND order_cost <= 120 ) THEN  
        SET cost_bucket = 'Medium';  
    ELSEIF order_cost > 120 THEN  
        SET cost_bucket = 'High';  
    END IF;  
    RETURN (cost_bucket);  
END;

-- Example: Find the order cost distribution across each week by low, medium and high bucket

-- SELECT 
--     WEEK_NUMBER,
-- 	orderCostBucket(ORDER_COST) COST_BUCKET, 
--     COUNT(*) CNT 
-- FROM gl_eats_cust_ord_v 
-- GROUP BY 1,2;
