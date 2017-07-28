CREATE DATABASE  IF NOT EXISTS `Ascott_InvMgmt`
USE `Ascott_InvMgmt`;


CREATE TABLE `Items` (
  `iid` int(11) NOT NULL UNIQUE AUTO_INCREMENT,
  `name` char(45) NOT NULL UNIQUE,
  `category` char(25) NOT NULL,
  `picture` char(50) NOT NULL,
  `price` DECIMAL(13,4) CHECK (`price` >= 0.0000),
  `reorder_pt` int(11) NOT NULL,
  `out_by` char(20) NOT NULL, 
  `in_by` char(20) NOT NULL, 
  `in_out_ratio` float(5, 4) NOT NULL CHECK(`in_out_ratio` >= 0), 
  `remarks` varchar(255),
  PRIMARY KEY (`iid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `User` (
  `username` varchar(45) NOT NULL UNIQUE,
  `password` varchar(256) NOT NULL,
  `role` varchar(15) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`username`),
  KEY (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Permissions` (
  `role` VARCHAR(15) NOT NULL,
  `stock_in` BOOLEAN NOT NULL,
  `admin` BOOLEAN NOT NULL,
  PRIMARY KEY (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `TagInfo` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` char(50) NOT NUlL,
  `storeroom` char(45) NOT NULL,
  `remarks` varchar(255),
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS TagItems (
  iid int(11) NOT NULL,
    tag int(11) NOT NULL,
    qty_left int(8) NOT NULL CHECK (qty >= 0),
    PRIMARY KEY (iid, tag),
    FOREIGN KEY (iid) REFERENCES Items(iid) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE `Logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` char(45) NOT NULL,
  `date_time` datetime NOT NULL,
  `action` char(45) NOT NULL, 
  `qty_moved` int(45) NOT NULL,
  `qty_left` int(45) NOT NULL,
  `item` int(11) NOT NULL,
  `location` char(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE OR REPLACE VIEW view_item_locations AS 
SELECT Items.*, TagItems.tag, TagItems.qty_left
FROM Items INNER JOIN TagItems 
ON Items.iid = TagItems.iid;