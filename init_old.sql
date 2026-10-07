-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Sep 25, 2025 at 10:00 AM
-- Server version: 8.0.43
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `evbox_manager`
--
CREATE DATABASE IF NOT EXISTS `evbox_manager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `evbox_manager`;

-- --------------------------------------------------------

--
-- Table structure for table `chargeSessions`
--

CREATE TABLE `chargeSessions` (
  `sessionID` int NOT NULL,
  `passNumber` int NOT NULL,
  `sessionStart` datetime NOT NULL,
  `sessionEnd` datetime NOT NULL,
  `energyUsage` int NOT NULL,
  `EVBOXNumber` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `electricityPrice`
--

CREATE TABLE `electricityPrice` (
  `logTime` datetime NOT NULL,
  `price` decimal(4,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `EVBoxes`
--

CREATE TABLE `EVBoxes` (
  `EVBOXID` int NOT NULL,
  `isUsed` tinyint(1) NOT NULL DEFAULT '0',
  `locationID` int NOT NULL,
  `softwareVersion` int NOT NULL,
  `isOnline` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `EVBoxes`
--

INSERT INTO `EVBoxes` (`EVBOXID`, `isUsed`, `locationID`, `softwareVersion`, `isOnline`) VALUES
(1, 1, 1, 1, 1),
(2, 0, 1, 1, 1),
(3, 0, 2, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `locationID` int NOT NULL,
  `locationName` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`locationID`, `locationName`) VALUES
(1, 'Gebouw A'),
(2, 'Gebouw B');

-- --------------------------------------------------------

--
-- Table structure for table `userPas`
--

CREATE TABLE `userPas` (
  `userID` int NOT NULL,
  `passNumber` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `userPas`
--

INSERT INTO `userPas` (`userID`, `passNumber`) VALUES
(1, '04BA2A2ADA1790');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` int NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `adress` varchar(50) NOT NULL,
  `zipcode` varchar(8) NOT NULL,
  `country` varchar(2) NOT NULL,
  `firstName` varchar(30) NOT NULL,
  `tussenvoegsel` varchar(10) NOT NULL,
  `lastName` varchar(30) NOT NULL,
  `phonenumber` int NOT NULL,
  `bankaccount` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `email`, `password`, `adress`, `zipcode`, `country`, `firstName`, `tussenvoegsel`, `lastName`, `phonenumber`, `bankaccount`, `role`) VALUES
(1, 'alice@example.com', 'scrypt:32768:8:1$Kj5kf932ZErLm2fs$51b62472f62eff7e16749574f4e9efdac8bdd23198941c69f3ff7b81c283cffafc3e214af782914b9bf902b04d8bfec3beb06507cc11103b082b7f813fb723db', '123 Main Street', '12345', 'NL', 'Alice', '', 'Smith', 1234567890, 'NL12BANK1234567890', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `EVBoxes`
--
ALTER TABLE `EVBoxes`
  ADD PRIMARY KEY (`EVBOXID`),
  ADD KEY `locationID` (`locationID`);

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`locationID`);

--
-- Indexes for table `userPas`
--
ALTER TABLE `userPas`
  ADD PRIMARY KEY (`passNumber`),
  ADD KEY `userID` (`userID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `EVBoxes`
--
ALTER TABLE `EVBoxes`
  MODIFY `EVBOXID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `locationID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
