-- dummy data for storing items in more than one location
INSERT INTO TagItems VALUES
	(2, 9, 6),
    (8, 9, 9),
    (10, 9, 36);
    
    
-- Creates a view to find all the items which are stored in more than one location
CREATE OR REPLACE VIEW view_item_locations AS 
SELECT Items.*, TagItems.tag, TagItems.qty_left
FROM Items INNER JOIN TagItems 
ON Items.iid = TagItems.iid;

SELECT * FROM view_item_locations;

-- UPDATE TagItems SET qty_left=84 WHERE iid=8 AND location='Level5C3';