-- MySQL dump 10.13  Distrib 8.4.11, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dismat_magazzino
-- ------------------------------------------------------
-- Server version	8.4.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dismat_magazzino`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dismat_magazzino` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `dismat_magazzino`;

--
-- Table structure for table `articolo`
--

DROP TABLE IF EXISTS `articolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articolo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codice` varchar(30) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `descrizione` text,
  `quantita` decimal(10,2) NOT NULL DEFAULT '0.00',
  `scorta_minima` decimal(10,2) NOT NULL DEFAULT '0.00',
  `unita_misura` varchar(20) NOT NULL,
  `categoria_id` int NOT NULL,
  `attivo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `codice` (`codice`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `articolo_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articolo`
--

LOCK TABLES `articolo` WRITE;
/*!40000 ALTER TABLE `articolo` DISABLE KEYS */;
INSERT INTO `articolo` VALUES (1,'ART001','Guanti in nitrile','Guanti monouso per attività di laboratorio',80.00,20.00,'pz',1,1),(2,'ART002','Tasselli Fischer Duopower','Tasselli per ancoraggio a cartongessi',9500.00,500.00,'pz',1,1),(3,'ART003','SET tasselli chimici','Tasselli chimici con ancoraggio Cogen',202.00,30.00,'pz',1,1),(4,'ART004','Set rivestimento Beton','beton per ancoraggio',20.00,1.00,'pz',1,1),(5,'ART005','Hydro monoelastico','granulare',20.00,1.00,'pz',1,1),(6,'TP001','Trapano Parkside','',1.00,1.00,'pz',1,0);
/*!40000 ALTER TABLE `articolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articolo_fornitore`
--

DROP TABLE IF EXISTS `articolo_fornitore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articolo_fornitore` (
  `articolo_id` int NOT NULL,
  `fornitore_id` int NOT NULL,
  PRIMARY KEY (`articolo_id`,`fornitore_id`),
  KEY `fornitore_id` (`fornitore_id`),
  CONSTRAINT `articolo_fornitore_ibfk_1` FOREIGN KEY (`articolo_id`) REFERENCES `articolo` (`id`),
  CONSTRAINT `articolo_fornitore_ibfk_2` FOREIGN KEY (`fornitore_id`) REFERENCES `fornitore` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articolo_fornitore`
--

LOCK TABLES `articolo_fornitore` WRITE;
/*!40000 ALTER TABLE `articolo_fornitore` DISABLE KEYS */;
INSERT INTO `articolo_fornitore` VALUES (1,1),(6,2),(3,3),(3,4);
/*!40000 ALTER TABLE `articolo_fornitore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descrizione` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Materiale di consumo','Materiali utilizzati nelle attività di laboratorio');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fornitore`
--

DROP TABLE IF EXISTS `fornitore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornitore` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ragione_sociale` varchar(120) NOT NULL,
  `referente` varchar(100) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornitore`
--

LOCK TABLES `fornitore` WRITE;
/*!40000 ALTER TABLE `fornitore` DISABLE KEYS */;
INSERT INTO `fornitore` VALUES (1,'Forniture Tecniche SRL','Mario Rossi','0922123456','info@fornituretecniche.it'),(2,' SicilTech SRL',' Anna Bianchi','0911234567','info@siciltech.it'),(3,'Cogen SRL','Mauro Bocci','3298077110','bocci85@gmail.com'),(4,'Fischer Italia SRL','Paolo Mendola','3297890667','paolomendola@outlook.it'),(5,'Licata SPA','Marcella Giunta','3286080889','marcellalicata@gmail.com');
/*!40000 ALTER TABLE `fornitore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foto_articolo`
--

DROP TABLE IF EXISTS `foto_articolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foto_articolo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `articolo_id` int NOT NULL,
  `nome_file` varchar(255) NOT NULL,
  `didascalia` varchar(255) DEFAULT NULL,
  `principale` tinyint(1) NOT NULL DEFAULT '0',
  `attiva` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `articolo_id` (`articolo_id`),
  CONSTRAINT `foto_articolo_ibfk_1` FOREIGN KEY (`articolo_id`) REFERENCES `articolo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foto_articolo`
--

LOCK TABLES `foto_articolo` WRITE;
/*!40000 ALTER TABLE `foto_articolo` DISABLE KEYS */;
INSERT INTO `foto_articolo` VALUES (1,1,'a2479e32a9e2439e90aa48102f24542c_guanti.jpeg','Guanti in nitrile, nero.(M/L)',0,0),(2,1,'4f54c9ac9c8b4a41b04dac1b60f8c898_guanti-in-nitrile.jpeg','Guanti in nitrile, nero.(M/L)',1,1),(3,2,'0fc58a46c75a4fcfa2319f1dd8f8cca5_tassellifischer.jpeg','',0,0),(4,2,'363b4447cf2c4e55a3eeded458f4db41_tasselliuso.jpeg','uso',0,1),(5,2,'89b6cabc61674cc3baef4311150b0601_tass.jpeg','',1,1),(6,3,'85fd63ff175942f88454723a418e36b0_settassellichimici.jpeg','',1,1),(7,4,'269c4df5a65041e8a0dbc2d3344712a5_setrivestimentobetonperancoraggio.jpeg','',1,1),(8,5,'a00ef95163394c0a972fa75b589f8a42_hydromonoelasticolicata.jpeg','',1,1),(9,6,'c3923a976125474dbc300eb4b9d687ee_trapano.jpeg','',1,1);
/*!40000 ALTER TABLE `foto_articolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimento`
--

DROP TABLE IF EXISTS `movimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `articolo_id` int NOT NULL,
  `utente_id` int NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `quantita` decimal(10,2) NOT NULL,
  `data_movimento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `articolo_id` (`articolo_id`),
  KEY `utente_id` (`utente_id`),
  CONSTRAINT `movimento_ibfk_1` FOREIGN KEY (`articolo_id`) REFERENCES `articolo` (`id`),
  CONSTRAINT `movimento_ibfk_2` FOREIGN KEY (`utente_id`) REFERENCES `utente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimento`
--

LOCK TABLES `movimento` WRITE;
/*!40000 ALTER TABLE `movimento` DISABLE KEYS */;
INSERT INTO `movimento` VALUES (1,1,2,'ENTRATA',10.00,'2026-09-18 09:18:28','test entrata'),(2,1,2,'ENTRATA',2.00,'2026-09-18 09:26:22',''),(3,1,2,'USCITA',12.00,'2026-09-18 10:05:54','test uscita'),(4,2,2,'USCITA',500.00,'2026-09-22 11:23:36','Ritirati per campata di ancoraggio'),(5,5,1,'ENTRATA',7.00,'2026-09-22 11:24:39','incremento scorta'),(6,3,1,'ENTRATA',2.00,'2026-09-22 11:25:05','omaggio cogen');
/*!40000 ALTER TABLE `movimento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utente`
--

DROP TABLE IF EXISTS `utente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utente`
--

LOCK TABLES `utente` WRITE;
/*!40000 ALTER TABLE `utente` DISABLE KEYS */;
INSERT INTO `utente` VALUES (1,'lara','pbkdf2:sha256:1000000$oSQrEfBwcN6rXAeb$226bd1698b9242e0fe1b44b9dfe9024507f9eebb1040518c1ae3934bc20e9298','Lara Maria Cigna'),(2,'test','pbkdf2:sha256:1000000$xkQ59mDyMkVjsZHh$33d653aa75027edafcf3a94620cbb9b7cd3ad0258ef643a833bc0b4fd46a9432','test');
/*!40000 ALTER TABLE `utente` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-14 18:19:12
