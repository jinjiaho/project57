# Script for database changes

CREATE TABLE TagItems SELECT sku, location, qty_left FROM Items;
SELECT * from TagItems;

LOCK TABLES TagItems WRITE;
/*!40000 ALTER TABLE TagItems DISABLE KEYS */;
ALTER TABLE TagItems CHANGE COLUMN sku iid INT(11) NOT NULL;
ALTER TABLE TagItems ADD PRIMARY KEY (iid, location), 
ADD CONSTRAINT CHECK(qty >= 0);
UNLOCK TABLES;

LOCK TABLES Items WRITE;
/*!40000 ALTER TABLE Items DISABLE KEYS */;
ALTER TABLE Items CHANGE COLUMN sku iid INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE Items DROP PRIMARY KEY, 
ADD PRIMARY KEY (iid), 
DROP COLUMN location, 
DROP COLUMN qty_left, 
ADD COLUMN price DECIMAL(13,4);
UNLOCK TABLES;

SELECT * FROM TagItems;
SELECT * FROM Items;

CREATE TABLE IF NOT EXISTS PriceChange (
	item INT(11) NOT NULL,
    old_price DECIMAL(13,4),
    new_price DECIMAL(13,4),
    date_effective DATETIME NOT NULL,
    PRIMARY KEY (item, date_effective)
);
SELECT * FROM PriceChange;

SELECT COUNT(iid), location FROM TagItems GROUP BY location;

LOCK TABLES Items WRITE;
ALTER TABLE Items CHANGE COLUMN `category` `category` char(25) NOT NULL;
UNLOCK TABLES;