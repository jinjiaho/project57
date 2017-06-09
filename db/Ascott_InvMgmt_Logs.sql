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
-- Table structure for table `Logs`
--

DROP TABLE IF EXISTS `Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(45) NOT NULL,
  `date_time` datetime NOT NULL,
  `action` char(45) NOT NULL, -- 'out', 'in' or 'check' --
  `qty_moved` int(45) NOT NULL,
  `qty_left` int(45) NOT NULL,
  `item` varchar(45) NOT NULL,
  `location` varchar(45) NOT NULL,
  FOREIGN KEY (`user`) references User (`username`) on delete cascade on update cascade,
  FOREIGN KEY (`item`) references Item (`name`) on delete cascade on update cascade,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `Logs` WRITE;
/*!40000 ALTER TABLE `Logs` DISABLE KEYS */;
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('1', '1', '2016-12-19 09:04:00', 'out', '-12', '246', '9', '639');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('2', '1', '2016-12-20 00:51:00', 'out', '-11', '317', '9', '721');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('3', '2', '2016-12-24 03:55:00', 'out', '-11', '201', '9', '736');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('4', '2', '2016-12-25 00:20:00', 'in', '500', '500', '4', '635');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('5', '3', '2016-12-29 17:35:00', 'out', '-13', '452', '4', '506');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('6', '0', '2016-12-29 18:26:00', 'out', '-13', '258', '9', '967');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('7', '3', '2016-12-30 00:51:00', 'out', '-8', '481', '4', '931');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('8', '1', '2016-12-30 09:04:00', 'out', '-20', '428', '4', '13');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('9', '1', '2016-12-30 17:35:00', 'out', '0', '465', '4', '7');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('10', '3', '2016-12-31 00:20:00', 'in', '340', '340', '9', '272');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('11', '1', '2017-01-01 00:50:00', 'out', '-11', '489', '4', '909');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('12', '0', '2017-01-01 11:40:00', 'out', '-17', '411', '4', '471');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('13', '1', '2017-01-01 17:34:00', 'out', '-16', '465', '4', '509');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('14', '1', '2017-01-01 18:26:00', 'out', '0', '448', '4', '173');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('15', '4', '2017-01-02 16:24:00', 'out', '-15', '186', '9', '501');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('16', '3', '2017-01-02 18:23:00', 'out', '-4', '448', '4', '605');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('17', '1', '2017-01-03 00:20:00', 'in', '100', '100', '1', '589');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('18', '0', '2017-01-04 03:55:00', 'out', '-2', '389', '4', '760');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('19', '3', '2017-01-04 11:58:00', 'out', '-6', '405', '4', '445');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('20', '2', '2017-01-04 13:00:00', 'out', '-11', '212', '9', '544');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('21', '4', '2017-01-05 00:50:00', 'out', '-3', '97', '1', '408');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('22', '2', '2017-01-05 00:51:00', 'out', '-2', '95', '1', '69');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('23', '4', '2017-01-05 17:34:00', 'out', '-2', '93', '1', '945');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('24', '2', '2017-01-05 17:35:00', 'out', '-8', '85', '1', '699');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('25', '2', '2017-01-05 17:35:00', 'out', '-7', '78', '1', '465');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('26', '3', '2017-01-05 18:23:00', 'out', '-7', '71', '1', '169');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('27', '4', '2017-01-05 18:26:00', 'out', '-7', '64', '1', '612');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('28', '4', '2017-01-06 09:04:00', 'out', '-7', '57', '1', '894');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('29', '4', '2017-01-06 13:00:00', 'out', '-14', '391', '4', '341');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('30', '2', '2017-01-09 11:40:00', 'out', '-8', '49', '1', '906');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('31', '3', '2017-01-09 11:58:00', 'out', '-13', '223', '9', '722');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('32', '0', '2017-01-10 11:58:00', 'out', '-8', '41', '1', '229');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('33', '3', '2017-01-10 13:00:00', 'out', '-8', '33', '1', '313');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('34', '4', '2017-01-11 05:30:00', 'out', '-3', '380', '4', '148');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('35', '4', '2017-01-11 05:30:00', 'out', '-14', '172', '9', '993');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('36', '1', '2017-01-13 03:55:00', 'out', '-5', '28', '1', '333');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('37', '0', '2017-01-14 01:54:00', 'out', '-3', '377', '4', '482');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('38', '0', '2017-01-14 16:24:00', 'out', '-6', '383', '4', '814');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('39', '0', '2017-01-16 16:24:00', 'out', '-1', '27', '1', '720');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('40', '2', '2017-01-18 05:30:00', 'out', '-7', '20', '1', '642');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('41', '4', '2017-01-18 10:44:00', 'out', '-19', '358', '4', '421');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('42', '2', '2017-01-20 09:28:00', 'out', '-19', '339', '4', '212');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('43', '2', '2017-01-21 01:54:00', 'out', '-2', '18', '1', '350');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('44', '4', '2017-01-22 00:50:00', 'out', '-12', '328', '9', '71');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('45', '0', '2017-01-23 10:44:00', 'in', '100', '118', '1', '537');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('46', '0', '2017-01-23 18:20:00', 'out', '-19', '313', '4', '292');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('47', '1', '2017-01-24 09:28:00', 'out', '-4', '114', '1', '127');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('48', '4', '2017-01-24 18:23:00', 'out', '-11', '271', '9', '190');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('49', '2', '2017-01-25 11:40:00', 'out', '-10', '236', '9', '87');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('50', '4', '2017-01-26 17:34:00', 'out', '-11', '306', '9', '543');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('51', '3', '2017-01-27 12:19:00', 'out', '-7', '332', '4', '154');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('52', '2', '2017-01-28 03:22:00', 'out', '-11', '289', '4', '286');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('53', '4', '2017-01-28 07:24:00', 'out', '-1', '300', '4', '564');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('54', '0', '2017-01-30 12:19:00', 'out', '-2', '112', '1', '466');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('55', '0', '2017-02-01 14:39:00', 'out', '-12', '301', '4', '198');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('56', '2', '2017-02-01 18:20:00', 'out', '-2', '110', '1', '410');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('57', '3', '2017-02-02 20:35:00', 'out', '-14', '232', '9', '343');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('58', '3', '2017-02-03 01:54:00', 'out', '-10', '162', '9', '846');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('59', '3', '2017-02-03 14:39:00', 'out', '-5', '105', '1', '690');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('60', '3', '2017-02-03 17:35:00', 'out', '-10', '282', '9', '524');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('61', '0', '2017-02-04 07:24:00', 'out', '-6', '99', '1', '9');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('62', '1', '2017-02-04 17:35:00', 'out', '-14', '292', '9', '552');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('63', '4', '2017-02-05 03:22:00', 'out', '-7', '92', '1', '282');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('64', '0', '2017-02-05 10:44:00', 'in', '-15', '147', '9', '978');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('65', '1', '2017-02-06 04:59:00', 'out', '-13', '276', '4', '317');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('66', '1', '2017-02-07 12:17:00', 'out', '-14', '262', '4', '20');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('67', '0', '2017-02-09 20:35:00', 'out', '-18', '231', '4', '304');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('68', '1', '2017-02-11 16:46:00', 'out', '-9', '222', '4', '6');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('69', '4', '2017-02-13 04:59:00', 'out', '-4', '88', '1', '596');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('70', '3', '2017-02-14 08:59:00', 'out', '-11', '198', '9', '57');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('71', '0', '2017-02-14 21:56:00', 'out', '-13', '249', '4', '949');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('72', '1', '2017-02-15 09:28:00', 'out', '-11', '136', '9', '244');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('73', '2', '2017-02-15 12:17:00', 'out', '-2', '86', '1', '260');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('74', '4', '2017-02-16 18:20:00', 'out', '-15', '111', '9', '968');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('75', '1', '2017-02-17 21:56:00', 'out', '-8', '78', '1', '158');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('76', '3', '2017-02-17 21:56:00', 'out', '-15', '246', '9', '497');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('77', '1', '2017-02-18 20:35:00', 'out', '-7', '71', '1', '814');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('78', '3', '2017-02-19 07:24:00', 'out', '-14', '86', '9', '233');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('79', '2', '2017-02-19 16:46:00', 'out', '-7', '64', '1', '122');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('80', '4', '2017-02-20 04:59:00', 'out', '-15', '61', '9', '247');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('81', '1', '2017-02-20 15:48:00', 'out', '-13', '209', '4', '170');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('82', '2', '2017-02-20 15:48:00', 'out', '-12', '209', '9', '877');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('83', '3', '2017-02-22 15:48:00', 'out', '-6', '58', '1', '485');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('84', '2', '2017-02-24 10:23:00', 'out', '-14', '146', '9', '495');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('85', '1', '2017-02-25 12:19:00', 'out', '-10', '126', '9', '592');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('86', '3', '2017-02-26 08:59:00', 'out', '-17', '192', '4', '460');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('87', '2', '2017-02-26 14:39:00', 'out', '-11', '100', '9', '940');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('88', '2', '2017-02-27 12:17:00', 'in', '200', '261', '9', '500');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('89', '4', '2017-02-28 02:37:00', 'out', '-11', '181', '4', '679');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('90', '1', '2017-02-28 08:59:00', 'out', '-4', '54', '1', '80');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('91', '1', '2017-03-02 03:19:00', 'out', '-14', '132', '9', '639');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('92', '4', '2017-03-04 03:48:00', 'out', '-11', '121', '9', '355');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('93', '0', '2017-03-05 03:22:00', 'out', '-10', '76', '9', '447');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('94', '2', '2017-03-05 09:34:00', 'out', '-20', '161', '4', '11');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('95', '3', '2017-03-06 02:37:00', 'out', '-6', '48', '1', '387');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('96', '2', '2017-03-07 10:23:00', 'out', '-10', '151', '4', '88');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('97', '4', '2017-03-08 02:45:00', 'out', '0', '181', '4', '317');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('98', '1', '2017-03-09 02:37:00', 'out', '-13', '185', '9', '538');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('99', '3', '2017-03-09 09:34:00', 'out', '-11', '160', '9', '853');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('100', '1', '2017-03-10 02:45:00', 'out', '-5', '43', '1', '878');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('101', '1', '2017-03-10 03:19:00', 'out', '-14', '137', '4', '264');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('102', '1', '2017-03-10 09:34:00', 'out', '-4', '39', '1', '271');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('103', '1', '2017-03-13 21:25:00', 'out', '-12', '71', '9', '716');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('104', '2', '2017-03-14 10:23:00', 'out', '-5', '34', '1', '221');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('105', '2', '2017-03-15 03:48:00', 'out', '-4', '133', '4', '146');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('106', '0', '2017-03-15 16:46:00', 'out', '-11', '221', '9', '697');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('107', '1', '2017-03-17 05:32:00', 'out', '-15', '118', '4', '954');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('108', '0', '2017-03-18 03:19:00', 'out', '-2', '32', '1', '324');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('109', '2', '2017-03-21 03:48:00', 'out', '-8', '24', '1', '3');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('110', '4', '2017-03-22 15:05:00', 'out', '-10', '24', '9', '332');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('111', '3', '2017-03-23 02:45:00', 'out', '-14', '171', '9', '92');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('112', '4', '2017-03-23 05:32:00', 'out', '-7', '17', '1', '880');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('113', '2', '2017-03-24 16:32:00', 'out', '-16', '102', '4', '1');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('114', '4', '2017-03-25 22:31:00', 'out', '-14', '45', '9', '100');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('115', '2', '2017-03-26 16:32:00', 'out', '-8', '9', '1', '859');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('116', '3', '2017-03-26 20:25:00', 'out', '-1', '69', '4', '711');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('117', '0', '2017-03-27 11:34:00', 'out', '-12', '90', '4', '777');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('118', '2', '2017-03-29 11:34:00', 'out', '-4', '5', '1', '891');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('119', '1', '2017-03-30 16:32:00', 'out', '-12', '96', '9', '468');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('120', '2', '2017-03-30 21:25:00', 'out', '-20', '70', '4', '221');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('121', '1', '2017-03-31 04:09:00', 'in', '-11', '34', '9', '887');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('122', '4', '2017-04-01 21:25:00', 'out', '-2', '3', '1', '440');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('123', '4', '2017-04-02 04:09:00', 'out', '-11', '58', '4', '757');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('124', '3', '2017-04-02 20:25:00', 'out', '-3', '0', '1', '682');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('125', '0', '2017-04-03 05:32:00', 'out', '-13', '108', '9', '945');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('126', '2', '2017-04-03 15:05:00', 'in', '250', '308', '4', '357');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('127', '1', '2017-04-03 22:31:00', 'out', '0', '69', '4', '752');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('128', '0', '2017-04-05 22:31:00', 'out', '-8', '-8', '1', '79');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('129', '3', '2017-04-06 11:34:00', 'out', '-13', '83', '9', '201');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('130', '0', '2017-04-10 04:09:00', 'in', '150', '142', '1', '295');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('131', '1', '2017-04-10 09:47:00', 'out', '-14', '292', '4', '81');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('132', '4', '2017-04-10 15:05:00', 'out', '-1', '141', '1', '312');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('133', '4', '2017-04-11 01:31:00', 'out', '-2', '306', '4', '253');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('134', '1', '2017-04-11 02:34:00', 'out', '-20', '272', '4', '951');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('135', '3', '2017-04-13 01:31:00', 'out', '-1', '140', '1', '165');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('136', '0', '2017-04-13 07:51:00', 'out', '-6', '266', '4', '274');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('137', '1', '2017-04-14 19:26:00', 'out', '-2', '264', '4', '296');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('138', '0', '2017-04-16 09:47:00', 'out', '-3', '137', '1', '917');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('139', '1', '2017-04-16 20:25:00', 'out', '-12', '59', '9', '793');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('140', '4', '2017-04-18 02:34:00', 'out', '-4', '133', '1', '604');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('141', '0', '2017-04-18 18:01:00', 'out', '-5', '259', '4', '37');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('142', '1', '2017-04-19 07:51:00', 'out', '-1', '132', '1', '627');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('143', '0', '2017-04-19 19:26:00', 'out', '-2', '130', '1', '552');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('144', '3', '2017-04-20 07:51:00', 'out', '-11', '90', '9', '164');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('145', '0', '2017-04-21 09:53:00', 'out', '-3', '256', '4', '182');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('146', '2', '2017-04-21 13:16:00', 'out', '-14', '213', '9', '776');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('147', '2', '2017-04-24 07:55:00', 'out', '-14', '188', '9', '475');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('148', '2', '2017-04-24 18:01:00', 'out', '-2', '128', '1', '185');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('149', '0', '2017-04-25 02:03:00', 'out', '-19', '237', '4', '498');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('150', '1', '2017-04-25 09:47:00', 'out', '-11', '1', '9', '251');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('151', '4', '2017-04-26 01:31:00', 'out', '-12', '12', '9', '299');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('152', '0', '2017-04-26 09:53:00', 'out', '-6', '122', '1', '448');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('153', '0', '2017-04-26 10:26:00', 'out', '-11', '226', '4', '701');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('154', '0', '2017-04-28 07:49:00', 'out', '-5', '210', '4', '276');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('155', '0', '2017-04-28 09:18:00', 'out', '-4', '222', '4', '473');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('156', '3', '2017-04-28 18:06:00', 'out', '-14', '192', '4', '454');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('157', '2', '2017-04-30 02:03:00', 'out', '-3', '119', '1', '103');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('158', '4', '2017-05-01 10:26:00', 'out', '-3', '116', '1', '894');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('159', '4', '2017-05-02 13:49:00', 'out', '-4', '206', '4', '356');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('160', '2', '2017-05-03 09:18:00', 'out', '-3', '113', '1', '81');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('161', '3', '2017-05-04 07:55:00', 'out', '0', '210', '4', '956');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('162', '2', '2017-05-04 13:16:00', 'out', '-7', '215', '4', '493');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('163', '2', '2017-05-05 17:16:00', 'out', '-16', '156', '4', '952');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('164', '2', '2017-05-06 03:19:00', 'out', '-20', '172', '4', '759');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('165', '3', '2017-05-06 13:16:00', 'out', '-2', '111', '1', '50');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('166', '4', '2017-05-07 02:34:00', 'in', '100', '101', '9', '499');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('167', '0', '2017-05-07 07:49:00', 'out', '-5', '106', '1', '414');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('168', '0', '2017-05-07 07:55:00', 'out', '-6', '100', '1', '590');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('169', '3', '2017-05-07 13:49:00', 'out', '-3', '97', '1', '48');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('170', '1', '2017-05-07 18:06:00', 'out', '-3', '94', '1', '400');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('171', '3', '2017-05-07 18:06:00', 'out', '-13', '164', '9', '375');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('172', '3', '2017-05-08 02:03:00', 'out', '-12', '255', '9', '137');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('173', '1', '2017-05-08 10:26:00', 'out', '-15', '240', '9', '149');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('174', '0', '2017-05-10 03:19:00', 'out', '-8', '86', '1', '335');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('175', '0', '2017-05-11 17:16:00', 'out', '-2', '84', '1', '354');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('176', '0', '2017-05-11 19:12:00', 'out', '0', '156', '4', '287');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('177', '4', '2017-05-12 07:49:00', 'out', '-11', '202', '9', '847');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('178', '0', '2017-05-13 06:53:00', 'out', '-20', '128', '4', '411');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('179', '2', '2017-05-13 16:10:00', 'out', '-6', '148', '4', '453');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('180', '4', '2017-05-14 12:27:00', 'out', '-2', '154', '4', '410');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('181', '4', '2017-05-14 19:12:00', 'out', '-10', '127', '9', '560');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('182', '0', '2017-05-15 18:01:00', 'out', '-10', '67', '9', '710');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('183', '0', '2017-05-16 19:12:00', 'out', '-7', '77', '1', '785');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('184', '0', '2017-05-16 19:26:00', 'out', '-13', '77', '9', '540');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('185', '4', '2017-05-18 12:27:00', 'out', '-1', '76', '1', '759');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('186', '4', '2017-05-20 16:10:00', 'out', '-2', '74', '1', '576');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('187', '1', '2017-05-23 06:53:00', 'out', '-8', '66', '1', '160');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('188', '1', '2017-05-24 03:19:00', 'out', '-15', '149', '9', '493');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('189', '1', '2017-05-25 09:53:00', 'in', '200', '267', '9', '985');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('190', '4', '2017-05-29 13:49:00', 'out', '-11', '177', '9', '304');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('191', '3', '2017-06-01 17:16:00', 'out', '-12', '137', '9', '640');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('192', '4', '2017-06-02 09:18:00', 'out', '-13', '227', '9', '600');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('193', '4', '2017-06-03 16:10:00', 'out', '-12', '104', '9', '749');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('194', '4', '2017-06-07 12:27:00', 'out', '-11', '116', '9', '50');
INSERT INTO `ascott_invmgmt`.`logs` (`id`, `user`, `date_time`, `action`, `qty_moved`, `qty_left`, `item`, `location`) VALUES ('195', '2', '2017-06-08 06:53:00', 'out', '-13', '91', '9', '64');
/*!40000 ALTER TABLE `Logs` ENABLE KEYS */;
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
