-- This reate a trigger to decrease the quantity of
-- an item after adding a new order.
CREATE TRIGGER lower_quantity_item
AFTER INSERT
ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE NAME = NEW.item_name;
