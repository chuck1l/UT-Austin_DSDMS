-- Clear the temp table for each cycle
TRUNCATE temp_t;
-- Load the new data into temp_t from the csv files, changing the quarter number (file name) as needed
LOAD DATA LOCAL INFILE '/Users/chucks_apple/Documents/UT-Austin_DSDMS/sql_and_databases/new_wheels_proj/Data/new_wheels_sales_qtr_4.csv'
INTO TABLE temp_t
FIELDS TERMINATED by ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Start mysql in terminal if you get errors
-- enter in terminal: SET global LOCAL_INFILE=1;
-- enter in connection (advanced): OPT_LOCAL_INFILE=1
-- Close and reopen MySQL Workbench

-- Call all of the stored procedures
CALL vehicle_p();
CALL customer_p();
CALL order_p();
CALL product_p();
CALL shipper_p();