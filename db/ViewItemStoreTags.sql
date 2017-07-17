CREATE OR REPLACE VIEW view_itemStoreTags AS
SELECT Items.name, TagInfo.tname, TagInfo.storeroom
FROM Items INNER JOIN TagItems
ON Items.iid = TagItems.iid
INNER JOIN TagInfo
ON TagItems.tag = TagInfo.tid;

SELECT * FROM view_itemStoreTags;