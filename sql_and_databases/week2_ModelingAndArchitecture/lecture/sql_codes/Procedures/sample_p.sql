-- Create a sample table
CREATE TABLE sample_t (
	col1 INTEGER,
	col2 VARCHAR(10)
	);

-- Write a procedure to append a row with an integer and a varchar value 
DELIMITER $$
CREATE PROCEDURE sample_p(A INTEGER, B VARCHAR(10))
BEGIN
	INSERT INTO sample_t (col1, col2) VALUES (A,B);
END;

-- Call procedures and test with different parameters
CALL sample_p(1,'a');
SELECT * FROM sample_t;

CALL sample_p(2,'b');
SELECT * FROM sample_t;

CALL sample_p(3,'c');
SELECT * FROM sample_t;
