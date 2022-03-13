-- [1] How many Orders do we get each week? What is the trend across weeks?
SELECT
	WEEK_NUMBER,
    COUNT(*) AS NUMBER_OF_ORDERS
FROM GL_EATS_ORD_T
GROUP BY 1;

-- [2] Is our average Delivery Rating decreasing across weeks?
SELECT
	WEEK_NUMBER,
    AVG(STAR_RATING) AS AVERAGE_DELIVERY_RATING
FROM GL_EATS_DEL_T
GROUP BY 1;

-- [3] What is the average Order Cost each week? Is it trending upwards or downwards?
SELECT
	WEEK_NUMBER,
    AVG(ORDER_COST) AS AVERAGE_ORDER_COST
FROM GL_EATS_ORD_T
GROUP BY 1;

-- [4] How has employee performance been by week? (average number of deliveries per week)
SELECT
	DELIVERY_EMP_ID,
    WEEK_NUMBER,
    COUNT(ORDER_ID) AS NUMBER_OF_ORDERS_DELIVERED
FROM GL_EATS_DEL_ORD_V
GROUP BY 1,2
ORDER BY 1,2 ASC, 3 DESC;

-- [5] What is the Week-over-Week % of Revenue?
WITH WoW AS 
(
	SELECT
		WEEK_NUMBER,
		SUM(calcRevenue(ORDER_COST, DISCOUNT, DELIVERY_STATUS)) REVENUE
	FROM 
		GL_EATS_DEL_ORD_V
	GROUP BY 1
)
SELECT
	WEEK_NUMBER,
    REVENUE,
    LAG(REVENUE) OVER (ORDER BY WEEK_NUMBER) AS PREVIOUS_WEEK_REVENUE,
    ((REVENUE - LAG(REVENUE) OVER (ORDER BY WEEK_NUMBER))/LAG(REVENUE) OVER(ORDER BY WEEK_NUMBER) * 100) AS "WEEK OVER WEEK REVENUE(%)"
FROM
	WoW;

-- [6] Who are the high and low-performing employees? (Average delivery rating per week)
SELECT
	DELIVERY_EMP_ID,
    WEEK_NUMBER,
    AVG(STAR_RATING) AS AVERAGE_DELIVERY_RATING
FROM  GL_EATS_DEL_ORD_V
GROUP BY 1,2
ORDER BY 1,2 ASC, 3 DESC;

-- [7] What is the cancellation rate of a customer?
SELECT 
	CUSTOMER_ID, 
    COUNT(*) TOTAL_ORDERS,
    SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) CANCELLATIONS,
    SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) / COUNT(*) AS "CANCELLATION_RATE(%)"
FROM GL_EATS_DEL_ORD_V
GROUP BY 1
ORDER BY 4 DESC;

-- [8] What is the distribution of employees in a locality?
SELECT 
	REST.LOCALITY,
    COUNT(DEL.DELIVERY_EMP_ID) AS NUMBER_OF_DELIVERY_EMPLOYEES
FROM GL_EATS_REST_T REST
JOIN GL_EATS_DEL_T DEL
USING(RESTAURANT_ID)
GROUP BY 1;

-- [9] What is the average rating by a customer?
SELECT 
	CUSTOMER_ID,
    AVG(STAR_RATING) as AVERAGE_RATING
FROM GL_EATS_DEL_ORD_V
GROUP BY 1;

-- [10] Do Customers who get a higher Discount tend to give a higher Delivery Rating?
/* Hint: Create 2 buckets:
[1] discount bucket: LOW(>=15,<=18), MEDIUM(>=19,<=21), HIGH(>=22)
[2] star rating bucket: LOW(1,2), MEDIUM(3,4), HIGH(5)
Then count the instances where discount = HIGH and star rating = HIGH and see if it is a significant number */
WITH DISCOUNT_BUCKET AS
(
	SELECT
    CUSTOMER_ID,
    ORDER_ID,
        CASE 
			WHEN DISCOUNT >=15 AND DISCOUNT <=18 THEN "LOW"
            WHEN DISCOUNT >=19 AND DISCOUNT <=21 THEN "MEDIUM"
            WHEN DISCOUNT >=22 THEN "HIGH"
		END AS DISC_BUCKET,
        CASE 
			WHEN STAR_RATING <= 2 THEN "LOW" 
            WHEN STAR_RATING >= 3 AND STAR_RATING <= 4 THEN "MEDIUM"
            WHEN STAR_RATING = 5 THEN "HIGH"
		END AS DELIVERY_RATING_BUCKET
	FROM
		GL_EATS_DEL_ORD_V
)
SELECT
	DISC_BUCKET,
    DELIVERY_RATING_BUCKET,
    COUNT(DELIVERY_RATING_BUCKET) AS "DELIVERY_RATING"
FROM DISCOUNT_BUCKET
WHERE DISC_BUCKET = "HIGH"
GROUP BY 1,2;

/* Observation: If you find the ratio of (HIGH discount and HIGH rating) / (Total Ratings where the HIGH discount was given), you see
   that this ratio is not very large. Hence, you cannot conclusively say, that giving customers HIGH discounts will attract
   HIGH ratings. */
    
-- [11] How many Employees are overworked and delivering above the acceptable limit? (at least 150 orders and above per week)
SELECT
	DELIVERY_EMP_ID, 
    WEEK_NUMBER, 
    COUNT(ORDER_ID) AS NUMBER_OF_DELIVERIES
FROM GL_EATS_DEL_ORD_V  
GROUP BY 1,2
HAVING COUNT(ORDER_ID) >= 150;

-- [12] Who are the customers not satisfied with the service? (Average Delivery Rating <= 3)
SELECT
	CUSTOMER_ID,
    AVG(STAR_RATING) AS AVERAGE_DELIVERY_RATING
FROM GL_EATS_DEL_ORD_V
GROUP BY 1
HAVING AVG(STAR_RATING) <= 3;

-- [13] Which Cities are our Vendor Restaurants located in? What is the distribution?
SELECT
	CITY_NAME,
    COUNT(RESTAURANT_ID) AS NUMBER_OF_RESTAURANTS
FROM GL_EATS_REST_T
GROUP BY 1;

-- [14] Are there specific cities that have a high rate of cancellation? (greater than or equal to 10%)
SELECT
	CITY_NAME,
    COUNT(*) TOTAL_ORDERS,
    SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) CANCELLED_ORDERS, 
	SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) / COUNT(*) RATE_OF_CANCELLATIONS
FROM GL_EATS_DEL_REST_V
GROUP BY 1
HAVING RATE_OF_CANCELLATIONS >= 0.1
ORDER BY 4 DESC; 

-- [15] What is the distribution of Customers by Order Frequency across cities?
SELECT
	CUSTOMER_ID,
    WEEK_NUMBER,
	CITY,
    COUNT(ORDER_ID) AS NUMBER_OF_ORDERS
FROM
	GL_EATS_ORD_REST_V
GROUP BY 1,2;

-- [16] How many customers have used our services so far, across Countries?
SELECT 
	COUNTRY_CODE,
    COUNT(DISTINCT CUSTOMER_ID) AS NUMBER_OF_CUSTOMERS
FROM GL_EATS_ORD_REST_V
GROUP BY 1
ORDER BY 2 DESC;

-- [17] What is the average Order Quantity each week? Is it trending upwards or downwards?
SELECT 
	WEEK_NUMBER,
    AVG(ORDER_ITEMS)
FROM GL_EATS_CUST_ORD_V
GROUP BY 1;
 
-- [18] Which are my high revenue-generating restaurants?
SELECT
	DELORD.RESTAURANT_ID,
    DELREST.RESTAURANT_NAME,
    SUM(calcRevenue(DELORD.ORDER_COST, DELORD.DISCOUNT, DELORD.DELIVERY_STATUS)) REVENUE
FROM GL_EATS_DEL_ORD_V AS DELORD
JOIN GL_EATS_DEL_REST_V AS DELREST
ON DELORD.ORDER_ID = DELREST.ORDER_ID
GROUP BY 1
ORDER BY 3 DESC;

-- [19] Are cancellations more likely to come from low-rated restaurants? 
-- Hint: 
	-- Categorize rating into low (<=3), medium (>3, <4) and high (>=4, <=5)
	-- Get the ratio of cancelled orders by total orders and see if they are consistent or skewed towards a single category
SELECT 
    CASE 
		WHEN RESTAURANT_RATING <= 3 THEN "LOW"
		WHEN RESTAURANT_RATING > 3 AND RESTAURANT_RATING < 4  THEN "MEDIUM"
		WHEN RESTAURANT_RATING >= 4 AND RESTAURANT_RATING <= 5  THEN "HIGH"
	END AS RATING_BUCKET,
    SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) CANCALLED_ORDERS,
    COUNT(*) TOTAL_ORDERS,
    (SUM(CASE WHEN DELIVERY_STATUS = 4 THEN 1 ELSE 0 END) / COUNT(*) * 100) CANCELLATION_RATE,
    AVG(RESTAURANT_RATING) AVG_REST_RATING
FROM GL_EATS_DEL_REST_V
GROUP BY 1;

-- Conclusion: Order cancellation does not depend on the rating of the restaurant


