-- This create a trigger to reset valid_email
-- only when email has been changed
DELIMITER //
CREATE TRIGGER update_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- This check if the email has been changed
    IF NEW.email != OLD.email THEN
        -- This reset the valid_email attribute
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;
