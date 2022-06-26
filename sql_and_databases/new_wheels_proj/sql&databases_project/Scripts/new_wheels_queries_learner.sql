/* QUESTIONS RELATED TO CUSTOMERS */

-- [Q1] What is the distribution of customers across states?
-- Simple groub by and count of distinct customers
-- Don't want to double count repeat customers, using distinct

SELECT 
	STATE
    , COUNT(DISTINCT CUSTOMER_ID) AS customer_count
FROM vehdb.veh_ord_cust_v
GROUP BY 1
ORDER BY 2 DESC;

-- [Q2] What is the average rating in each quarter?
-- Very Bad is 1, Bad is 2, Okay is 3, Good is 4, Very Good is 5.
-- Changing the quarter from integer to the string because I think it reports better
-- Could have used a case statement for the numeric feedback but used an additional function for fun
-- Rounding just to manage significant figures of results

SELECT 
	CASE
		WHEN QUARTER_NUMBER = 1 THEN '1st Quarter'
        WHEN QUARTER_NUMBER = 2 THEN '2nd Quarter'
        WHEN QUARTER_NUMBER = 3 THEN '3rd Quarter'
        WHEN QUARTER_NUMBER = 4 THEN '4th Quarter'
	END AS yearly_quarter
    , ROUND(AVG(NUMERIC_FEEDBACK),2) AS average_rating
FROM vehdb.veh_ord_cust_v
GROUP BY QUARTER_NUMBER
ORDER BY QUARTER_NUMBER; 

-- [Q3] Are customers getting more dissatisfied over time?
-- I could group by only date for this problem, but thought it would be interesting to see it more as a scatter
-- Selecting Shipping date rather than order date because I assume that its closer to when they'd actually give feedback
-- Rounding just to manage significant figures of results

SELECT
	SHIP_DATE
    , CUSTOMER_ID
    , ROUND(AVG(NUMERIC_FEEDBACK),2) AS average_feedback
FROM vehdb.veh_ord_cust_v
GROUP BY 1, 2
ORDER BY 1;

-- I want to view the results both ways
SELECT
	SHIP_DATE
    , ROUND(AVG(NUMERIC_FEEDBACK),2) AS average_feedback
FROM vehdb.veh_ord_cust_v
GROUP BY 1
ORDER BY 1;

-- One more look
SELECT 
	SUBSTRING(SHIP_DATE, 1, 7) AS date_mo
    , ROUND(AVG(CASE WHEN CUSTOMER_FEEDBACK = 'Very Bad' THEN 1 ELSE 0 END),2) AS very_bad_rating_avg
    , ROUND(AVG(CASE WHEN CUSTOMER_FEEDBACK = 'Bad' THEN 1 ELSE 0 END),2) AS bad_rating_avg
    , ROUND(AVG(CASE WHEN CUSTOMER_FEEDBACK = 'Okay' THEN 1 ELSE 0 END),2) AS Okay_rating_avg
    , ROUND(AVG(CASE WHEN CUSTOMER_FEEDBACK = 'Good' THEN 1 ELSE 0 END),2) AS good_rating_avg
    , ROUND(AVG(CASE WHEN CUSTOMER_FEEDBACK = 'Very Good' THEN 1 ELSE 0 END),2) AS very_good_rating_avg
FROM vehdb.veh_ord_cust_v
GROUP BY 1
ORDER BY 1;

-- [Q4] Which are the top 5 vehicle makers preferred by the customer.
-- Viewed the sixth results just to see if it was a tie between 5 and 6
-- I will remove the sixth from the visual in the report

SELECT
	VEHICLE_MAKER
    , COUNT(DISTINCT CUSTOMER_ID) AS num_customers
FROM veh_prod_cust_v 
GROUP BY 1
ORDER BY 2 DESC
LIMIT 6;

-- [Q5] What is the most preferred vehicle make in each state?
-- Interesting results, multiple ties in many states
-- That will be communicated in the report

SELECT
	prveh.STATE
    , prveh.VEHICLE_MAKER
    , order_rank
    , order_volume
FROM (
	SELECT
		STATE
		, VEHICLE_MAKER
		, RANK() OVER 
		(PARTITION BY STATE ORDER BY COUNT(DISTINCT ORDER_ID) DESC) AS order_rank
        , COUNT(DISTINCT ORDER_ID) AS order_volume
	FROM veh_prod_cust_v
    GROUP BY 1, 2
    ) prveh
WHERE prveh.order_rank = 1;


/* QUESTIONS RELATED TO REVENUE and ORDERS */

-- [Q6] What is the trend of number of orders by quarters?
-- Changing the quarter from integer to the string because I think it reports better
-- Used count distinct knowing that it has a very high probability of be unnecessary
-- Just being overly cautious

SELECT
	CASE
		WHEN QUARTER_NUMBER = 1 THEN '1st Quarter'
        WHEN QUARTER_NUMBER = 2 THEN '2nd Quarter'
        WHEN QUARTER_NUMBER = 3 THEN '3rd Quarter'
        WHEN QUARTER_NUMBER = 4 THEN '4th Quarter'
	END AS yearly_quarter
    , COUNT(DISTINCT ORDER_ID) AS order_volume
FROM vehdb.veh_ord_cust_v
GROUP BY QUARTER_NUMBER
ORDER BY QUARTER_NUMBER; 

-- [Q7] What is the quarter over quarter % change in revenue?
-- Utilizing a case statement here to prevent the first quarter having an odd result
-- We don't have results from q4 last year so it would be 100%.... rather see 0% change
-- Changing the quarter from integer to the string because I think it reports better

SELECT
	qoq.yearly_quarter
    , CASE
		WHEN qoq.yearly_quarter = '1st Quarter' THEN 0.00 -- 0% change due to no prior data
        ELSE ROUND((qoq.current_revenue - qoq.prior_revenue)/qoq.current_revenue, 2)
	END AS q_over_q_revenue_change
FROM(
	SELECT
		CASE
			WHEN ocv.QUARTER_NUMBER = 1 THEN '1st Quarter'
			WHEN ocv.QUARTER_NUMBER = 2 THEN '2nd Quarter'
			WHEN ocv.QUARTER_NUMBER = 3 THEN '3rd Quarter'
			WHEN ocv.QUARTER_NUMBER = 4 THEN '4th Quarter'
		END AS yearly_quarter
		, SUM(ocv.REVENUE) AS current_revenue
        , LAG(SUM(ocv.REVENUE), 1, 0) OVER(ORDER BY ocv.QUARTER_NUMBER) AS prior_revenue
    FROM vehdb.veh_ord_cust_v ocv
    GROUP BY ocv.QUARTER_NUMBER
    ORDER BY ocv.QUARTER_NUMBER
) qoq;
    

-- [Q8] What is the trend of revenue and orders by quarters?
-- Changing the quarter from integer to the string because I think it reports better


SELECT
	CASE
		WHEN QUARTER_NUMBER = 1 THEN '1st Quarter'
        WHEN QUARTER_NUMBER = 2 THEN '2nd Quarter'
        WHEN QUARTER_NUMBER = 3 THEN '3rd Quarter'
        WHEN QUARTER_NUMBER = 4 THEN '4th Quarter'
	END AS yearly_quarter
    , COUNT(DISTINCT ORDER_ID) AS order_volume
    , SUM(REVENUE) AS total_revenue
FROM vehdb.veh_ord_cust_v
GROUP BY QUARTER_NUMBER
ORDER BY QUARTER_NUMBER; 

/* QUESTIONS RELATED TO SHIPPING */

-- [Q9] What is the average discount offered for different types of credit cards?
-- Rounding just to manage significant figures of results

SELECT
	CREDIT_CARD_TYPE
    , ROUND(AVG(DISCOUNT), 2) AS average_discount
FROM vehdb.veh_ord_cust_v
GROUP BY 1;

-- [Q10] What is the average time taken to ship the placed orders for each quarters?
-- Use days_to_ship_f function to compute the time taken to ship the orders.
-- Changing the quarter from integer to the string because I think it reports better
-- Rounding just to manage significant figures of results

SELECT
	CASE
		WHEN QUARTER_NUMBER = 1 THEN '1st Quarter'
        WHEN QUARTER_NUMBER = 2 THEN '2nd Quarter'
        WHEN QUARTER_NUMBER = 3 THEN '3rd Quarter'
        WHEN QUARTER_NUMBER = 4 THEN '4th Quarter'
	END AS yearly_quarter
    , ROUND(AVG(SHIPPING_TIME),2) AS average_shipping_time
FROM vehdb.veh_ord_cust_v
GROUP BY QUARTER_NUMBER
ORDER BY QUARTER_NUMBER;
	