-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: Ascott_InvMgmt
-- ------------------------------------------------------
-- Server version	5.7.18

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
-- Dumping data for table `Items`
--

USE `Ascott_InvMgmt`;
LOCK TABLES `Items` WRITE;
/*!40000 ALTER TABLE `Items` DISABLE KEYS */;
INSERT INTO `Items` VALUES (1,'Butternut Squash','Level4C2',35,0,1,'Guest Hampers','Butternut Squash.jpg','Per Pkt'),(2,'Snapple Juice','Level4C2',48,0,1,'Guest Hampers','Snapple Juice.jpg','Per Bottle'),(3,'Cereals (small)','Level4C2',384,0,1,'Guest Hampers','Cereals (small).jpg','Per Pkt'),(4,'Raw Honey','Level5C3',12,0,1,'Guest Hampers','Raw Honey.jpg','Per Bt'),(5,'Honey Mustard Onion Chips','Level5C3',72,0,1,'Guest Hampers','Honey Mustard Onion Chips.jpg','Per Pkt'),(6,'Sea Salt Small Chips','Level5C3',48,0,1,'Guest Hampers','Sea Salt Small Chips.jpg','Per Pkt'),(7,'Farm Crackers','Level5C3',48,0,1,'Guest Hampers','Farm Crackers.jpg','Per Pkt'),(8,'Instant Oatmeal','Level5C3',60,0,1,'Guest Hampers','Instant Oatmeal.jpg','Per Pkt'),(9,'Ascott Teddy Grocery Bag','Level5C3',100,0,1,'Guest Hampers','Ascott Teddy Grocery Bag.jpg','Per Pcs'),(10,'Coffee Creamer','Level5C4',3,10,1,'Guest Hampers','Coffee Creamer.jpg','Per Box'),(11,'Coke zero (330ml)','Level5C4',18,0,24,'Guest Hampers','Coke zero (330ml).jpg','Per Carton'),(12,'Sprite (330ml)','Level5C4',5,6,24,'Guest Hampers','Sprite (330ml).jpg','Per Carton'),(13,'Coke zero (1.5L)','Level5C4',11,0,1,'Guest Hampers','Coke zero (1.5L).jpg','Per Btl'),(14,'Sprite (1.5L)','Level5C4',5,0,1,'Guest Hampers','Sprite (1.5L).jpg','Per Btl'),(15,'Dr.Who Water','Level5C4',18,100,24,'Guest Hampers','Dr.Who Water.png','Per Carton'),(16,'Fiji Water','Level5C4',300,20,24,'Guest Hampers','Fiji Water.jpg','Per Carton'),(17,'Golden crystal sugar','Level6C2',5,16,1,'Guest Hampers','Golden crystal sugar.jpg','Per Packet'),(18,'Toblerone Milk','Level6C2',24,84,1,'Guest Hampers','Toblerone Milk.jpg','Per Bar'),(19,'Nespresso Livanto','Level6C2',600,0,1,'Guest Hampers','Nespresso Livanto.jpg','Per Pcs'),(20,'Nespresso Ristretto','Level6C2',200,400,1,'Guest Hampers','Nespresso Ristretto.jpg','Per Pcs'),(21,'RIPE Sachet Sugar','Level6C2',6,0,1,'Guest Hampers','RIPE Sachet Sugar.jpg','Per Pkt'),(22,'TWG Earl Grey','Level6C2',3,9,24,'Guest Hampers','TWG Earl Grey.jpg','Per Carton'),(23,'TWG English breakfast Tea','Level6C2',3,9,24,'Guest Hampers','TWG English breakfast Tea.jpg','Per Carton'),(24,'TWG Jasmine Tea','Level6C2',7,0,24,'Guest Hampers','TWG Jasmine Tea.jpg','Per Carton'),(25,'Milk (1L)','Level6C2',10,0,24,'Guest Hampers','Milk (1L).jpg','Per Carton'),(26,'Wine','Level6C2',24,0,1,'Guest Hampers','Wine.jpg','Per Bottle'),(27,'Nescafe Gold Blend Dcf ','Level6C2',4,0,24,'Guest Hampers','Nescafe Gold Blend Dcf .jpg','Per Carton'),(28,'Ascott Cookies','Level6C2',200,0,1,'Guest Hampers','Ascott Cookies.jpg','Per Pcs'),(29,'Fish Noodle','Level6C2',2,3,24,'Guest Hampers','Fish Noodle.jpg','Per Carton'),(30,'Laksa Noodle','Level6C2',6,0,24,'Guest Hampers','Laksa Noodle.jpg','Per Carton'),(31,'Strawberry Jam','Level6C2',8,0,1,'Guest Hampers','Strawberry Jam.jpg','Per bottle'),(32,'Ascott Pen','Level4C2',300,171,1,'Guest Supplies','Ascott Pen.jpg','Per Pcs'),(33,'Umbrella','Level4C2',202,106,1,'Guest Supplies','Ascott umbrella.jpg','Per Pcs'),(34,'Laundry Bag','Level4C2',2000,639,1,'Guest Supplies','Laundry Bag.jpg','Per Pcs'),(35,'Laundry Bag(Plastic)','Level5C3',5000,2939,1,'Guest Supplies','Laundry bag plastic.jpg','Per Pcs'),(36,'Somat 3','Level5C3',3,1,24,'Guest Supplies','Somat 3.jpg','Per Carton'),(37,'Laundry Detergent-50g','Level5C3',1500,504,12,'Guest Supplies','Laundry detergent box.jpg','Per Box'),(38,'Hand Soap Bottle','Level5C3',100,65,1,'Guest Supplies','Hand soap bottle.jpg','Per Btl'),(39,'Dish Washing Bottle','Level5C3',384,237,1,'Guest Supplies','Dish washing bottle.jpg','Per Btl'),(40,'Toothbrush','Level5C3',500,134,1,'Guest Supplies','Toothbrush.jpg','Per Pcs'),(41,'Shaving Kit','Level5C4',3000,755,1,'Guest Supplies','Shaving kit.jpg','Per Pcs'),(42,'Shower Cap','Level5C4',4500,1449,1,'Guest Supplies','Shower cap.jpg','Per Pcs'),(43,'Comb','Level5C4',1500,397,1,'Guest Supplies','Comb.jpg','Per Pcs'),(44,'Cotton Buds','Level5C4',1500,404,1,'Guest Supplies','Cotton buds.jpg','Per Pcs'),(45,'Sewing Kit','Level5C4',11000,4491,1,'Guest Supplies','Sewing kit.jpg','Per Pcs'),(46,'Shampoo-35ml','Level5C4',3840,2115,1,'Guest Supplies','Shampoo 35ml.jpg','Per Btl'),(47,'Conditioner-35ml','Level5C4',2112,1147,1,'Guest Supplies','Conditioner 35ml.jpg','Per Btl'),(48,'Shower Gel-35ml','Level6C2',2880,1826,1,'Guest Supplies','Shower gel 35ml.jpg','Per Btl'),(49,'Body Lotion-35ml','Level6C2',3456,1907,1,'Guest Supplies','Body lotion 35ml.jpg','Per Btl'),(50,'Soap-50g','Level6C2',600,196,1,'Guest Supplies','Soap 50g.jpg','Per Pcs'),(51,'Soap -25g','Level6C2',1250,687,1,'Guest Supplies','Soap 25g.png','Per Pcs'),(52,'Tissue box','Level6C2',8,3,24,'Guest Supplies','Tissue box.jpg','Per Carton'),(53,'Toilet Roll','Level6C2',8,2,12,'Guest Supplies','Toilet Roll.jpg','Per Bundle'),(54,'Sanitary Bag','Level6C2',500,369,1,'Guest Supplies','Sanitary bag.jpg','Per Pcs'),(55,'Ascott gift L\'occitane','Level6C2',1224,362,1,'Guest Supplies','L\'occitaine.png','Per Pcs'),(56,'Bedroom Slippers','Level6C2',1800,1068,1,'Guest Supplies','Guest slippers.jpg','Per Pcs'),(57,'TEFAL VIESSE Electric kettle','B1C1',4,2,1,'Kitchenware','TEFAL VIESSE Electric kettle.jpg','Per Pcs'),(58,'BRAUN HT 400 Multitoast','B2C2',1,1,1,'Kitchenware','BRAUN HT 400 Multitoast.jpg','Per Pcs'),(59,'PADERNO ice bucket with Tong','B1C2',10,5,1,'Kitchenware','PADERNO ice bucket with Tong.jpg','Per Pcs'),(60,'PADERNO Sauce Pot with two handles and cover','B1C1',5,2,1,'Kitchenware','PADERNO Sauce Pot with two handles and cover.jpg','Per Pcs'),(61,'PADERNO sauce Pot with one handles and cover','B2C2',5,3,1,'Kitchenware','PADERNO sauce Pot with one handles and cover.jpg','Per Pcs'),(62,'PADERNO Frying Pan ','B1C2',1,1,1,'Kitchenware','PADERNO Frying Pan.jpg','Per Pcs'),(63,'PADERNO Soup Ladle','B1C5',3,2,1,'Kitchenware','PADERNO Soup Ladle.jpg','Per Pcs'),(64,'PADERNO Utility Knife','B1C4',20,10,1,'Kitchenware','PADERNO Utility Knife.jpg','Per Pcs'),(65,'PADERNO Parking /Fruit Knife','B1C2',30,8,1,'Kitchenware','PADERNO Parking Fruit Knife.jpg','Per Pcs'),(66,'PADERNO Potato Peeler','B1C1',23,7,1,'Kitchenware','PADERNO Potato Peeler.jpg','Per Pcs'),(67,'PADERNO Kitchen Scissors','B2C2',30,21,1,'Kitchenware','PADERNO Kitchen Scissors.jpg','Per Pcs'),(68,'PADERNO Can Opener','B1C2',33,18,1,'Kitchenware','PADERNO Can Opener.jpg','Per Pcs'),(69,'PADERNO Double Level Corkscrew','B1C1',35,19,1,'Kitchenware','PADERNO Double Level Corkscrew.jpg','Per Pcs'),(70,'PADERNO Kitchen Food Tong','B2C2',16,6,1,'Kitchenware','PADERNO Kitchen Food Tong.jpg','Per Pcs'),(71,'Wooden Pan Tuner / Spatula','B1C2',18,13,1,'Kitchenware','Wooden Pan Tuner Spatula.jpg','Per Pcs'),(72,'Kitchen Sponge Holder','B1C5',16,11,1,'Kitchenware','Kitchen Sponge Holder.jpg','Per Pcs'),(73,'Kitchen Sponge - 3m','B1C4',50,34,1,'Kitchenware','Kitchen Sponge - 3m.jpg','Per Pcs'),(74,'Kitchen Waste bin with lid','B1C2',4,2,1,'Kitchenware','Kitchen Waste bin with lid.jpg','Per Pcs'),(75,'Plastic Cutlery Tray ','B1C1',16,11,1,'Kitchenware','Plastic Cutlery Tray.jpg','Per Pcs'),(76,'Plastic Chopping Board','B2C2',12,9,1,'Kitchenware','Plastic Chopping Board.jpg','Per Pcs'),(77,'Hot Pot Mat','B1C2',96,65,1,'Kitchenware','Hot Pot Mat.jpg','Per Pcs'),(78,'Pot Holder / Oven Mitt','B1C1',43,32,1,'Kitchenware','Pot Holder Oven Mitt.jpg','Per Pcs'),(79,'RONA GLASS Scena-Crystalline Wine Glass','B2C2',30,10,1,'Kitchenware','RONA GLASS Scena-Crystalline Wine Glass.jpg','Per Pcs'),(80,'RONA GLASS Globo 12 High Ball Tumbler','B1C2',30,16,1,'Kitchenware','RONA GLASS Globo 12 High Ball Tumbler.jpg','Per Pcs'),(81,'RONA GLASS Globo 15 Cocktail Tumbler','B1C5',24,14,1,'Kitchenware','RONA GLASS Globo 15 Cocktail Tumbler.jpg','Per Pcs'),(82,'RONA GLASS Globo 16 Old-Fashioned Tumbler','B1C4',36,27,1,'Kitchenware','RONA GLASS Globo 16 Old-Fashioned Tumbler.jpg','Per Pcs'),(83,'SAMBONET Table / Dinner Knife','B1C2',39,21,1,'Kitchenware','SAMBONET Table Dinner Knife.jpg','Per Pcs'),(84,'SAMBONET Dessert Knife','B1C1',60,18,1,'Kitchenware','SAMBONET Dessert Knife.png','Per Pcs'),(85,'SAMBONET Table / Dinner Fork','B2C2',72,39,1,'Kitchenware','SAMBONET Table Dinner Fork.jpg','Per Pcs'),(86,'SAMBONET Dessert Fork','B1C2',75,44,1,'Kitchenware','SAMBONET Dessert Fork.jpg','Per Pcs'),(87,'SAMBONET Serving Spoon','B1C1',15,11,1,'Kitchenware','SAMBONET Serving Spoon.jpg','Per Pcs'),(88,'SAMBONET Table / Dinner Spoon','B2C2',82,48,1,'Kitchenware','SAMBONET Table Dinner Spoon.jpg','Per Pcs'),(89,'SAMBONET Dessert Spoon','B1C2',60,21,1,'Kitchenware','SAMBONET Dessert Spoon.jpg','Per Pcs'),(90,'SAMBONET Tea Spoon','B1C5',60,18,1,'Kitchenware','SAMBONET Tea Spoon.jpg','Per Pcs'),(91,'PANASONIC 1500W Hair Dryer','B1C4',114,29,1,'Kitchenware','PANASONIC 1500W Hair Dryer.jpg','Per Pcs'),(92,'NARUMI Ashtray','B1C2',99,35,1,'Kitchenware','NARUMI Ashtray.jpg','Per Pcs'),(93,'NARUMI 32cm Cosmo Oval Fish Platter','B1C1',7,2,1,'Kitchenware','NARUMI 32cm Cosmo Oval Fish Platter.jpg','Per Pcs'),(94,'NARUMI 27cm (Esprit) Dinner Plate','B2C2',17,11,1,'Kitchenware','NARUMI 27cm (Esprit) Dinner Plate.jpg','Per Pcs'),(97,'NARUMI 19cm Service Bowl','B2C2',15,4,1,'Kitchenware','NARUMI 19cm Service Bowl.jpg','Per Pcs'),(98,'NARUMI 10cm Chinese Rice Bowl','B1C2',18,12,1,'Kitchenware','NARUMI 10cm Chinese Rice Bowl.jpg','Per Pcs'),(99,'NARUMI Soup Spoon','B1C5',10,2,1,'Kitchenware','NARUMI Soup Spoon.jpg','Per Pcs'),(100,'NARUMI Coffee / Tea Pot','B1C4',2,2,1,'Kitchenware','NARUMI Coffee Tea Pot.jpg','Per Pcs'),(101,'NARUMI Milk / Creamer Jug','B1C2',7,2,1,'Kitchenware','NARUMI Milk Creamer Jug.jpg','Per Pcs'),(102,'NARUMI Sugar Pot with Cover','B1C1',4,2,1,'Kitchenware','NARUMI Sugar Pot with Cover.jpg','Per Pcs'),(103,'NARUMI Salt shaker','B2C2',15,4,1,'Kitchenware','NARUMI Salt shaker.jpg','Per Pcs'),(104,'NARUMI Pepper Shaker','B1C2',15,11,1,'Kitchenware','NARUMI Pepper Shaker.jpg','Per Pcs'),(105,'NARUMI Coffee Mug (Esprit)','B1C1',18,5,1,'Kitchenware','NARUMI Coffee Mug (Esprit).jpg','Per Pcs'),(106,'NARUMI Coffee / Tea Cup (Esprit)','B2C2',30,17,1,'Kitchenware','NARUMI Coffee Tea Cup (Esprit).jpg','Per Pcs'),(107,'NARUMI Coffee / Tea Cup Saucer','B1C2',16,6,1,'Kitchenware','NARUMI Coffee  Tea Cup Saucer.jpg','Per Pcs'),(108,'NARUMI Toothpick Holder','B1C5',15,6,1,'Kitchenware','NARUMI Toothpick Holder.jpg','Per Pcs'),(109,'Chopsticks','B1C4',62,21,1,'Kitchenware','Chopsticks.jpg','Per Pcs'),(110,'ILLUMINOR Torch,LED Light with bracket black','B1C2',2,2,1,'Kitchenware','ILLUMINOR Torch,LED Light with bracket black.jpg','Per Pcs'),(111,'Ironing Board ','B1C1',4,2,1,'Kitchenware','Ironing Board.jpg','Per Pcs'),(112,'Ironing Board cover','B2C2',24,7,1,'Kitchenware','Ironing Board cover.jpg','Per Pcs'),(113,'Ivory Satin Hanger with Chrome Plated','B1C2',98,58,1,'Kitchenware','Ivory Satin Hanger with Chrome Plated.jpg','Per Pcs'),(114,'Regular Wooden Hanger with anti-slip bar','B1C1',100,68,1,'Kitchenware','Regular Wooden Hanger with anti-slip bar.jpg','Per Pcs'),(115,'Trouser Hanger with notches and skirt clips','B2C2',90,43,1,'Kitchenware','Trouser Hanger with notches and skirt clips.jpg','Per Pcs'),(116,'Broad Coat Hanger','B1C2',50,31,1,'Kitchenware','Broad Coat Hanger.jpg','Per Pcs'),(117,'Iron - Tefal','B1C5',0,2,1,'Kitchenware','Iron - Tefal.jpg','Per Pcs'),(118,'IMPLUSE USA Resin Tissue Box Cover','B1C4',12,8,1,'Kitchenware','IMPLUSE USA Resin Tissue Box Cover.jpg','Per Pcs'),(119,'TANITA Precision Weighing Scale','B1C2',5,3,1,'Kitchenware','TANITA Precision Weighing Scale.jpg','Per Pcs'),(120,'PADERNO Meat Fork','B1C1',4,1,1,'Kitchenware','PADERNO Meat Fork.jpg','Per Pcs'),(121,'TEFAL/PHILIPS Rice and slow cooker','B2C2',0,2,1,'Kitchenware','TEFAL PHILIPS Rice and slow cooker.jpg','Per Pcs'),(122,'PADERNO Frying pan with cover','B1C2',1,2,1,'Kitchenware','PADERNO Frying pan with cover.jpg','Per Pcs'),(123,'Food strainer','B1C1',0,2,1,'Kitchenware','Food strainer.jpg','Per Pcs'),(124,'Nespresso coffee machine','B2C2',0,4,1,'Kitchenware','Nespresso coffee machine.jpg','Per Pcs');
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

-- Dump completed on 2017-05-31 14:27:31