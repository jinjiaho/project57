-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: Ascott_InvMgmt
-- ------------------------------------------------------
-- Server version	5.7.18


CREATE DATABASE  IF NOT EXISTS `Ascott_InvMgmt` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Ascott_InvMgmt`;
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `LocationInfo`
--

DROP TABLE IF EXISTS `LocationInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LocationInfo` (
  `name` char(50) NOT NUlL,
  `location` varchar(45) NOT NULL,
  `remarks` varchar(255),

  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `LocationInfo` WRITE;
/*!40000 ALTER TABLE `LocationInfo` DISABLE KEYS */;
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Kitchenware', 'B1', null);
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Chemical', 'Hskp Office', 'Daily linen movement');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Runner', '6th Floor', null);
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('L\'occitane', '7th Floor', 'Bathroom Amenities');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Extra Bed & Baby Cot', '9th Floor', null);
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Guest Supplies (10F)', '10th Floor', 'Amenities');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Guest Supplies (12F)', '12th Floor', 'Tissue roll & tissue box');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Guest Supplies (13F)', '13th Floor', 'Slippers');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Hamper', '15th Floor', 'F&B');
INSERT INTO `LocationInfo` (`name`, `location`, `remarks`) VALUES ('Linen', '17th Floor', 'New linen & towels');

/*!40000 ALTER TABLE `LocationInfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-21  2:32:05
/*
-- Query: SELECT * FROM Ascott_InvMgmt.LocationInfo
LIMIT 0, 1000

-- Date: 2017-06-19 23:27
*/

