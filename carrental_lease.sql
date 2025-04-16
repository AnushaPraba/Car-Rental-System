CREATE DATABASE  IF NOT EXISTS `carrental` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `carrental`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: carrental
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `lease`
--

DROP TABLE IF EXISTS `lease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lease` (
  `leaseID` int NOT NULL AUTO_INCREMENT,
  `vehicleID` int DEFAULT NULL,
  `customerID` int DEFAULT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `type` enum('DailyLease','MonthlyLease') NOT NULL,
  `expectedAmount` decimal(10,2) DEFAULT NULL,
  `paymentStatus` varchar(10) DEFAULT 'unpaid',
  PRIMARY KEY (`leaseID`),
  KEY `vehicleID` (`vehicleID`),
  KEY `customerID` (`customerID`),
  CONSTRAINT `lease_ibfk_1` FOREIGN KEY (`vehicleID`) REFERENCES `vehicle` (`vehicleID`),
  CONSTRAINT `lease_ibfk_2` FOREIGN KEY (`customerID`) REFERENCES `customer` (`customerID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease`
--

LOCK TABLES `lease` WRITE;
/*!40000 ALTER TABLE `lease` DISABLE KEYS */;
INSERT INTO `lease` VALUES (1,4,1,'2025-04-10','2025-04-10','DailyLease',1200.00,'paid'),(4,2,1,'2024-03-01','2024-03-10','DailyLease',10000.00,'paid'),(5,3,6,'2024-03-15','2024-04-15','MonthlyLease',28500.00,'unpaid'),(6,5,8,'2024-04-01','2024-04-07','DailyLease',10500.00,'paid'),(8,5,1,'2025-04-11','2025-04-12','DailyLease',3000.00,'unpaid'),(10,4,1,'2025-04-11','2025-04-12','DailyLease',2400.00,'paid'),(12,3,10,'2025-04-15','2025-04-17','DailyLease',2850.00,'unpaid'),(13,2,11,'2025-04-16','2025-04-16','DailyLease',1000.00,'unpaid');
/*!40000 ALTER TABLE `lease` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-16 17:50:07
