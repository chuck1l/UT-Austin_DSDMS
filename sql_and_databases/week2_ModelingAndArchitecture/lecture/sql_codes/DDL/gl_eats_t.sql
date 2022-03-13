DROP DATABASE IF EXISTS GL_EATS;
CREATE DATABASE GL_EATS;
USE gl_eats;

CREATE TABLE gl_eats_t (
	WEEK_NUMBER INTEGER,
        CUSTOMER_ID INTEGER,
	CUSTOMER_NAME VARCHAR(20),
	COUNTRY_CD VARCHAR(25),
	EMAIL_ADDRESS VARCHAR(50),
	ORDER_ID INTEGER,
	ORDER_COST INTEGER,
	ORDER_ITEMS INTEGER,
	DISCOUNT INTEGER,
	DELIVERY_EMP_ID INTEGER,
	DELIVERY_ID INTEGER,
	STAR_RATING INTEGER,
	DELIVERY_STATUS INTEGER,
	RESTAURANT_ID INTEGER,
	RESTAURANT_NAME VARCHAR(50),
	CITY_NAME VARCHAR(60),
	ADDRESS VARCHAR(100),
	LOCALITY VARCHAR(60),
	LONGITUDE DECIMAL(14,8),
	LATITUDE DECIMAL(14,8),
	CUISINES VARCHAR(100),
	RESTAURANT_RATING DECIMAL(2,1),
	PRIMARY KEY (ORDER_ID, RESTAURANT_ID, DELIVERY_ID, CUSTOMER_ID)
);

-- DROP TABLE gl_eats_t;