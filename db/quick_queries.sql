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
SELECT * FROM User;

CREATE TABLE PriceChange (
	item INT(11) NOT NULL,
    old_price DECIMAL(13,4),
    new_price DECIMAL(13,4),
    date_effective DATETIME NOT NULL,
    PRIMARY KEY (item, date_effective)
);

INSERT INTO Ascott_InvMgmt.TagItems VALUES (20, 11, 20);
UPDATE TagItems SET qty_left = 2 WHERE iid=20;
COMMIT;