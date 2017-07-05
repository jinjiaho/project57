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
-- Table structure for table `Items`
--

DROP TABLE IF EXISTS `Items`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Items` (
  `iid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `category` char(25) NOT NULL,
  `picture` char(50) NOT NULL,
  `price` DECIMAL(13,4),
  `reorder_pt` int(11) NOT NULL,
  `out_by` char(20) NOT NULL, -- usually carton
  `in_by` char(20) NOT NULL, -- usually carton
  `in_out_ratio` float(5, 4) NOT NULL, -- How many outs for one in
  PRIMARY KEY (`iid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `Items` WRITE;
/*!40000 ALTER TABLE `Items` DISABLE KEYS */;
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('UHT Milk', 'Guest Hamper', 'Milk.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Nespresso Livanto', 'Guest Hamper', 'Nespresso Livanto.jpg', 1, 'carton', 'pc', 0.005);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Nespresso Ristretto', 'Guest Hamper', 'Nespresso Ristretto.jpg', 1, 'carton', 'pc', 0.005);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Nescafe Gold', 'Guest Hamper', 'Nescafe Gold.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Sugar', 'Guest Hamper', 'Sugar.jpg', 1, 'packet', 'carton', 8.00);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Creamer', 'Guest Hamper', 'Creamer.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Milk', 'Guest Hamper', 'Milk.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Fiji Water', 'Guest Hamper', 'Fiji Water.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Dr. Who Water', 'Guest Hamper', 'Dr Who Water.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('TWG Earl Grey Tea', 'Guest Hamper', 'Earl Grey.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('TWG Jasmine Tea', 'Guest Hamper', 'Jasmine Tea.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('TWG English Breakfast Tea', 'Guest Hamper', 'English Breakfast Tea.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Iced Gems', 'Guest Hamper', 'Iced Gems.jpg', 1, 'tin', 'tin', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Wine', 'Guest Hamper', 'Wine.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Snapple Grape', 'Guest Hamper', 'Snapple Grape.jpg', 1, 'carton', 'carton', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Cheese Crackers', 'Guest Hamper', 'Cheese Crackers.jpg', 1, 'kg', 'kg', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Sea Salt Chocolate Cookies', 'Guest Hamper', 'Sea Salt Chocolate Cookies', 1, 'pc', 'pc', 1.0);
INSERT INTO `Items` (`name`, `category`, `picture`, `reorder_pt`, `out_by`, `in_by`, `in_out_ratio`) VALUES ('Glass Jar', 'Guest Hamper', 'Glass Jar.jpg', 1, 'carton', 'carton', 1.0);
/*!40000 ALTER TABLE `Items` ENABLE KEYS */;
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
