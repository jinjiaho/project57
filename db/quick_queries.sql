/*
LOCK TABLES Logs WRITE;
ALTER TABLE Logs ADD COLUMN remarks VARCHAR(255);
UNLOCK TABLES;
*/

SELECT * FROM view_item_locations;
SELECT * FROM TagItems;
SELECT * FROM TagInfo;
SELECT * FROM Items;
SELECT * FROM Logs;
SELECT * FROM Permissions;
SELECT * FROM PriceChange;
SELECT * FROM view_itemStoreTags;

