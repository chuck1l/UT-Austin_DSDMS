DROP DATABASE IF EXISTS covid_db;

CREATE DATABASE covid_db;
USE covid_db;

DROP TABLE IF EXISTS zone_stats;
CREATE TABLE zone_stats (
	timestamp DATETIME,
	zone_id VARCHAR(4),
	confirmed INTEGER,
	deaths INTEGER,
	recovered INTEGER,
	tested INTEGER,
	active INTEGER,
	need_hosp INTEGER,
	end_of_day INTEGER,
	PRIMARY KEY (timestamp)
);

DROP TABLE IF EXISTS requirements;
CREATE TABLE requirements (
	timestamp DATETIME,
	zone_id VARCHAR(4),
	beds_occupied INTEGER,
	beds_available INTEGER,
	beds_available_perc FLOAT,
	discharged INTEGER,
	o2_consumed INTEGER,
	o2_available INTEGER,
	o2_available_perc FLOAT,
	PRIMARY KEY (timestamp)
);

DROP TABLE IF EXISTS anomaly;
CREATE TABLE anomaly (
	timestamp DATETIME,
	zone_id VARCHAR(4),
	avg_confirmed FLOAT,
	PRIMARY KEY (timestamp)
);