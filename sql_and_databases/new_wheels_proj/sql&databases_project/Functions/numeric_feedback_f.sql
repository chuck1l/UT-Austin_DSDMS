-- This function takes the string based argument for feedback
-- Returns a value between 1 and 5, mapping

DELIMITER $$
CREATE FUNCTION getNumericFeedback(feedback VARCHAR(20))
RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE NUMERIC_FEEDBACK INT;
    IF feedback = 'Very Bad' THEN
		SET NUMERIC_FEEDBACK = 1;
	ELSEIF feedback = 'Bad' THEN
		SET NUMERIC_FEEDBACK = 2;
	ELSEIF feedback = 'Okay' THEN
		SET NUMERIC_FEEDBACK = 3;
	ELSEIF feedback = 'Good' THEN
		SET NUMERIC_FEEDBACK = 4;
	ELSEIF feedback = 'Very Good' THEN
		SET NUMERIC_FEEDBACK = 5;
	END IF;
    RETURN(NUMERIC_FEEDBACK);
END;