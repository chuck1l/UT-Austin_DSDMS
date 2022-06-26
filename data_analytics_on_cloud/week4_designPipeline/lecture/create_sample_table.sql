DROP DATABASE IF EXISTS mydb;

CREATE DATABASE mydb;
USE mydb;

DROP TABLE IF EXISTS sample_table;

CREATE TABLE sample_table (
    col1 INTEGER,
    col2 VARCHAR(4),
    col3 VARCHAR(4),
    col4 INTEGER,
	PRIMARY KEY (col1)
);