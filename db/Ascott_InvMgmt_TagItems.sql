DROP TABLE IF EXISTS TagItems;
CREATE TABLE IF NOT EXISTS TagItems (
	iid int(11) NOT NULL,
    tag int(11) NOT NULL,
    qty_left int(8) NOT NULL CHECK (qty >= 0),
    PRIMARY KEY (iid, tag)
);
-- iid: item id
-- tag: tag id
-- qty: number left in the store

LOCK TABLES TagItems WRITE;
INSERT INTO TagItems VALUES (1, 9, 38);
INSERT INTO TagItems VALUES (2, 9, 12);
INSERT INTO TagItems VALUES (3, 9, 1);
INSERT INTO TagItems VALUES (4, 9, 4);
INSERT INTO TagItems VALUES (5, 9, 20);
INSERT INTO TagItems VALUES (6, 9, 3);
INSERT INTO TagItems VALUES (7, 9, 10);
INSERT INTO TagItems VALUES (8, 9, 10);
INSERT INTO TagItems VALUES (9, 9, 9);
INSERT INTO TagItems VALUES (10, 9, 31);
INSERT INTO TagItems VALUES (11, 9, 13);
INSERT INTO TagItems VALUES (12, 9, 23);
INSERT INTO TagItems VALUES (13, 9, 3);
INSERT INTO TagItems VALUES (14, 9, 29);
INSERT INTO TagItems VALUES (15, 9, 20);
INSERT INTO TagItems VALUES (16, 9, 23);
INSERT INTO TagItems VALUES (17, 9, 2);
INSERT INTO TagItems VALUES (18, 9, 0);
UNLOCK TABLES;