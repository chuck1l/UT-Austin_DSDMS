TRUNCATE temp_t;
LOAD DATA LOCAL INFILE 'C:/Users/srivathskumar/Downloads/DSDMS/SQL/gl_eats_dump_week-2.csv' -- change this location to load another week
INTO TABLE temp_t
FIELDS TERMINATED by ','
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

/* This might fail due to Local Infile load restrictions set by default. Go to home on top left, right click on the connection, edit connection,
go to advanced, and in the others sections type OPT_LOCAL_INFILE=1 <please do not give spaces> */