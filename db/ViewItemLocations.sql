-- dummy data for storing items in more than one location
INSERT INTO TagItems VALUES
	(2, 'Level5C3', 6),
    (8, 'Level4C1', 9),
    (10, 'B1C2', 36),
    (45, 'B1C4', 7),
    (23, 'B2C2', 23),
    (87, 'Level4C1', 75),
    (14, 'Level5C3', 39),
    (83, 'Level5C3', 27),
    (96, 'Level6C2', 236);
    
    
-- Creates a view to find all the items which are stored in more than one location
CREATE VIEW view_item_locations AS 
SELECT Items.*, TagItems.location, TagItems.qty_left
FROM Items INNER JOIN TagItems 
ON Items.iid = TagItems.iid;

SELECT * FROM view_item_locations;

-- UPDATE TagItems SET qty_left=84 WHERE iid=8 AND location='Level5C3';