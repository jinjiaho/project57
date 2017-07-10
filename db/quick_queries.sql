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

INSERT INTO PriceChange VALUES (9, 0.00, 0.00, '2017-12-12 00:00:00');

INSERT INTO Ascott_InvMgmt.TagItems VALUES (16,7,7);
COMMIT;

INSERT INTO TagInfo ('tname', 'storeroom', 'remarks') VALUES ('Cats','10th Floor','cats');