-- Temp table utilized during ingestion, Qrt-By-Qrt

CREATE TABLE temp_t (
    SHIPPER_ID INTEGER,
    SHIPPER_NAME VARCHAR(50),
    SHIPPER_CONTACT_DETAILS VARCHAR(30),
    PRODUCT_ID INTEGER,
    VEHICLE_MAKER VARCHAR(60),
    VEHICLE_MODEL VARCHAR(60),
    VEHICLE_COLOR VARCHAR(60),
    VEHICLE_MODEL_YEAR INTEGER,
    VEHICLE_PRICE DECIMAL(14 , 2 ),
    QUANTITY INTEGER,
    DISCOUNT DECIMAL(4 , 2 ),
    CUSTOMER_ID VARCHAR(25),
    CUSTOMER_NAME VARCHAR(25),
    GENDER VARCHAR(15),
    JOB_TITLE VARCHAR(50),
    PHONE_NUMBER VARCHAR(20),
    EMAIL_ADDRESS VARCHAR(50),
    CITY VARCHAR(25),
    COUNTRY VARCHAR(40),
    STATE VARCHAR(40),
    CUSTOMER_ADDRESS VARCHAR(50),
    ORDER_DATE DATE,
    ORDER_ID VARCHAR(25),
    SHIP_DATE DATE,
    SHIP_MODE VARCHAR(25),
    SHIPPING VARCHAR(30),
    POSTAL_CODE INTEGER,
    CREDIT_CARD_TYPE VARCHAR(40),
    CREDIT_CARD_NUMBER BIGINT,
    CUSTOMER_FEEDBACK VARCHAR(20),
    QUARTER_NUMBER INTEGER,
    PRIMARY KEY (SHIPPER_ID, PRODUCT_ID, ORDER_ID, CUSTOMER_ID)
);