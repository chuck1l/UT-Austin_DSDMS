DROP DATABASE IF EXISTS dx_diag_db;

CREATE DATABASE dx_diag_db;
USE dx_diag_db;

DROP TABLE IF EXISTS dx_data;
CREATE TABLE dx_data (
	patient_id VARCHAR(5),
	timestamp DATETIME,
	o2_level INTEGER,
	heart_rate INTEGER,
	PRIMARY KEY (timestamp)
);

DROP TABLE IF EXISTS diag_metrics;
CREATE TABLE diag_metrics (
	patient_id VARCHAR(5),
	timestamp DATETIME,
	o2_level INTEGER,
	heart_rate INTEGER,
	avg_o2 FLOAT,
	avg_hr FLOAT,
	std_o2 FLOAT,
	std_hr FLOAT,
	min_o2 INTEGER,
	min_hr INTEGER,
	max_o2 INTEGER,
	max_hr INTEGER,
	PRIMARY KEY (timestamp)
);
