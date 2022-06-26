-- Populate the shipper table with the data from temp_t (calling from quarterly dump SQL)

DELIMITER $$
CREATE PROCEDURE shipper_p()
BEGIN
	INSERT INTO vehdb.shipper_t(
		SHIPPER_ID,
		SHIPPER_NAME,
		SHIPPER_CONTACT_DETAILS
    )
    SELECT DISTINCT
		SHIPPER_ID,
		SHIPPER_NAME,
		SHIPPER_CONTACT_DETAILS
	FROM vehdb.vehicle_t WHERE SHIPPER_ID NOT IN (SELECT DISTINCT SHIPPER_ID FROM vehdb.shipper_t);
END;