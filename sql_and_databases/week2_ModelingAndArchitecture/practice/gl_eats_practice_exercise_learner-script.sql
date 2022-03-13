-- [1] How many Orders do we get each week? What is the trend across weeks?

-- [2] Is our average Delivery Rating decreasing across weeks?

-- [3] What is the average Order Cost each week? Is it trending upwards or downwards?

-- [4] How has employee performance been by week? (average number of deliveries per week)

-- [5] What is the Week-over-Week % of Revenue?

-- [6] Who are the high and low-performing employees? (Average delivery rating per week)

-- [7] What is the cancellation rate of a customer?

-- [8] What is the distribution of employees in a locality?

-- [9] What is the average rating by a customer?

-- [10] Do Customers who get a higher Discount tend to give a higher Delivery Rating?
/* Hint: Create 2 buckets:
[1] discount bucket: LOW(>=15,<=18), MEDIUM(>=19,<=21), HIGH(>=22)
[2] star rating bucket: LOW(1,2), MEDIUM(3,4), HIGH(5)
Then count the instances where discount = HIGH and star rating = HIGH and see if it is a significant number */
    
-- [11] How many Employees are overworked and delivering above the acceptable limit? (at least 150 orders and above per week)

-- [12] Who are the customers not satisfied with the service? (Average Delivery Rating <= 3)

-- [13] Which Cities are our Vendor Restaurants located in? What is the distribution?

-- [14] Are there specific cities that have a high rate of cancellation? (greater than or equal to 10%)

-- [15] What is the distribution of Customers by Order Frequency across cities?

-- [16] How many customers have used our services so far, across Countries?

-- [17] What is the average Order Quantity each week? Is it trending upwards or downwards?
 
-- [18] Which are my high revenue-generating restaurants?

-- [19] Are cancellations more likely to come from low-rated restaurants? 
-- Hint: 
	-- Categorize rating into low (<=3), medium (>3, <4) and high (>=4, <=5)
	-- Get the ratio of cancelled orders by total orders and see if they are consistent or skewed towards a single category


