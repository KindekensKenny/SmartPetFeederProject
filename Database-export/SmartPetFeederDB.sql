-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: smartpetfeederdb
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acties`
--

DROP TABLE IF EXISTS `acties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Beschrijving` varchar(145) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acties`
--

LOCK TABLES `acties` WRITE;
/*!40000 ALTER TABLE `acties` DISABLE KEYS */;
INSERT INTO `acties` VALUES (1,'lichtintensiteit inlezen'),(2,'beweging detecteren'),(3,'motor draaien'),(4,'gewicht inlezen'),(5,'leds aan'),(6,'leds uit'),(7,'button ingedrukt');
/*!40000 ALTER TABLE `acties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Unit` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'LDR','FLOAT'),(2,'PIR','BOOLEAN'),(3,'HX711','FLOAT'),(4,'Motor','BOOLEAN'),(5,'LEDstrip','BOOLEAN');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `id` int NOT NULL AUTO_INCREMENT,
  `DeviceID` int DEFAULT NULL,
  `ActieID` int NOT NULL,
  `Datum` datetime NOT NULL,
  `Waarde` float DEFAULT NULL,
  `Beschrijving` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Historiek_Device_idx` (`DeviceID`),
  KEY `fk_Historiek_Acties1_idx` (`ActieID`),
  CONSTRAINT `fk_Historiek_Acties1` FOREIGN KEY (`ActieID`) REFERENCES `acties` (`id`),
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`DeviceID`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(2,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(3,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(4,5,5,'2021-05-27 14:55:00',1,'leds aan'),(5,5,6,'2021-05-29 01:12:00',0,'leds uit'),(6,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(7,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(8,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(9,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(10,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(11,5,5,'2021-05-27 14:55:00',1,'leds aan'),(12,5,6,'2021-05-29 01:12:00',0,'leds uit'),(13,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(14,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(15,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(16,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(17,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(18,5,5,'2021-05-27 14:55:00',1,'leds aan'),(19,5,6,'2021-05-29 01:12:00',0,'leds uit'),(20,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(21,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(22,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(23,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(24,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(25,5,5,'2021-05-27 14:55:00',1,'leds aan'),(26,5,6,'2021-05-29 01:12:00',0,'leds uit'),(27,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(28,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(29,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(30,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(31,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(32,5,5,'2021-05-27 14:55:00',1,'leds aan'),(33,5,6,'2021-05-29 01:12:00',0,'leds uit'),(34,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(35,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(36,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(37,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(38,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(39,5,5,'2021-05-27 14:55:00',1,'leds aan'),(40,5,6,'2021-05-29 01:12:00',0,'leds uit'),(41,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(42,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt'),(43,1,1,'2021-05-23 08:04:00',300,'lichtintensiteit inlezen'),(44,2,2,'2021-05-24 18:21:00',1,'beweging detecteren'),(45,3,4,'2021-05-26 04:38:00',15,'gewicht inlezen'),(46,5,5,'2021-05-27 14:55:00',1,'leds aan'),(47,5,6,'2021-05-29 01:12:00',0,'leds uit'),(48,4,3,'2021-05-30 11:29:00',NULL,'motor draaien'),(49,NULL,7,'2021-05-31 21:46:00',NULL,'button ingedrukt');
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-28 14:27:59
