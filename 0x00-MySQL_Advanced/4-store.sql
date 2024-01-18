-- This reate a trigger to decrease the quantity of
-- an item after adding a new order
DELIMITER //
CREATE TRIGGER decrease_quantity_item
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- This update the quantity of the corresponding item
    -- in the items table
    UPDATE items
    SET quantity = quantity - 1
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;
