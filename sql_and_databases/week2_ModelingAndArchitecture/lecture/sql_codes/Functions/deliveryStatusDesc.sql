-- DROP FUNCTION deliveryStatusDesc ;

DELIMITER $$  
CREATE FUNCTION deliveryStatusDesc(delivery_status INT)  
RETURNS VARCHAR(20)  
DETERMINISTIC  
BEGIN  
    DECLARE delivery_desc VARCHAR(20);  
    IF delivery_status = 1 THEN  
        SET delivery_desc = 'On-time Delivery';  
    ELSEIF delivery_status = 2 THEN  
        SET delivery_desc = 'Late Delivery';  
    ELSEIF delivery_status = 3 THEN  
        SET delivery_desc = 'Early Delivery';  
    ELSEIF delivery_status = 4 THEN   
	SET delivery_desc = 'Order Cancelled';  
    END IF;  
    RETURN (delivery_desc);  
END;

-- Example: Find out the distribution of the order status for each week

-- SELECT
-- 	WEEK_NUMBER,
-- 	deliveryStatusDesc(DELIVERY_STATUS) DELIVERY_STATUS, 
--     COUNT(*) CNT 
-- FROM gl_eats_del_ord_v 
-- GROUP BY 1,2;
