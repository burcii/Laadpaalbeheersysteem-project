-- ========================================
-- EVBox Charging System Database Schema
-- Clean, merged version (fixed)
-- ========================================

CREATE DATABASE IF NOT EXISTS `evbox_manager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `evbox_manager`;

-- Drop tables if they exist
DROP TABLE IF EXISTS chargeSessions;
DROP TABLE IF EXISTS electricityPrice;
DROP TABLE IF EXISTS userCards;
DROP TABLE IF EXISTS EVBoxes;
DROP TABLE IF EXISTS EVBOXLocations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS unregisteredUsers;

-- ========================================
-- 1. USERS TABLE
-- ========================================
CREATE TABLE users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    firstName VARCHAR(30) NOT NULL,
    nameParticle VARCHAR(10) DEFAULT '',
    lastName VARCHAR(30) NOT NULL,
    adress VARCHAR(100) NOT NULL,
    zipcode VARCHAR(10) NOT NULL,
    country VARCHAR(2) NOT NULL,
    phonenumber VARCHAR(20) NOT NULL,
    bankaccount VARCHAR(34) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'user',
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ========================================
-- 2. UNREGISTERED USERS (for pending or offline registrations)
-- ========================================
CREATE TABLE unregisteredUsers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    pass_number VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Actief'
);

-- ========================================
-- 3. EVBOX LOCATIONS
-- ========================================
CREATE TABLE EVBOXLocations (
    locationID INT PRIMARY KEY AUTO_INCREMENT,
    locationName VARCHAR(50) NOT NULL,
    address VARCHAR(100),
    city VARCHAR(50),
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 4. EVBOXES TABLE
-- ========================================
CREATE TABLE EVBoxes (
    EVBOXID INT PRIMARY KEY AUTO_INCREMENT,
    locationID INT NOT NULL,
    serialNumber VARCHAR(25) NOT NULL,
    softwareVersion VARCHAR(20) NOT NULL,
    status ENUM('Offline', 'Available', 'Ready', 'Charging', 'Cable Connected', 'Finished', 'Error', 'Maintainance') NOT NULL DEFAULT 'Offline',
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (locationID) REFERENCES EVBOXLocations(locationID)
);

-- ========================================
-- 5. USER CARDS TABLE
-- ========================================
CREATE TABLE userCards (
    cardID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    cardUID VARCHAR(25) NOT NULL UNIQUE,
    isActive TINYINT(1) NOT NULL DEFAULT 1,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
);

-- ========================================
-- 6. ELECTRICITY PRICE LOGGING
-- ========================================
CREATE TABLE electricityPrice (
    priceID INT PRIMARY KEY AUTO_INCREMENT,
    logTime DATETIME NOT NULL,
    price DECIMAL(10,4) NOT NULL,
    UNIQUE KEY unique_logtime (logTime)
);

-- ========================================
-- 7. CHARGING SESSIONS
-- ========================================
CREATE TABLE chargeSessions (
    sessionID INT PRIMARY KEY AUTO_INCREMENT,
    cardUID VARCHAR(25) NOT NULL,
    EVBOXID INT NOT NULL,
    locationName VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    sessionStart DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sessionEnd DATETIME NULL,
    energyUsage DECIMAL(10,2) NULL,
    totalCost DECIMAL(10,2) NULL,
    status ENUM('active', 'completed', 'failed', 'interrupted') NOT NULL DEFAULT 'active',
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cardUID) REFERENCES userCards(cardUID),
    FOREIGN KEY (EVBOXID) REFERENCES EVBoxes(EVBOXID)
);

-- ========================================
-- INDEXES
-- ========================================

CREATE INDEX idx_sessions_active ON chargeSessions(EVBOXID, sessionEnd);
CREATE INDEX idx_sessions_user ON chargeSessions(cardUID);
CREATE INDEX idx_electricity_time ON electricityPrice(logTime);

-- ========================================
-- SAMPLE DATA
-- ========================================
INSERT INTO users (email, password, firstName, nameParticle, lastName, adress, zipcode, country, phonenumber, bankaccount, role)
VALUES
('test@example.com', 'scrypt:32768:8:1$mMFdocahOPetdR3h$bce165fc3e420558bc1eb2e168d5f47d91f779c1383561b17c60524b0ca4b09d587a8efbe401f68b79db1aa95e874f324c019431fe2af7442fd2c8e42923cd26', 'Jan', 'de', 'Vries', 'Teststraat 1', '3511 AB', 'NL', '0612345678', 'NL91ABNA0417164300', 'user'),
('eva.muller@example.com', 'scrypt:32768:8:1$mMFdocahOPetdR3h$bce165fc3e420558bc1eb2e168d5f47d91f779c1383561b17c60524b0ca4b09d587a8efbe401f68b79db1aa95e874f324c019431fe2af7442fd2c8e42923cd26', 'Eva', '', 'Muller', 'Grote Markt 10', '9711 AB', 'NL', '0698765432', 'NL01INGB0001234567', 'user'),
('piet.admin@example.com', 'scrypt:32768:8:1$mMFdocahOPetdR3h$bce165fc3e420558bc1eb2e168d5f47d91f779c1383561b17c60524b0ca4b09d587a8efbe401f68b79db1aa95e874f324c019431fe2af7442fd2c8e42923cd26', 'Piet', 'van', 'Dijk', 'Hoofdstraat 55', '1012 EG', 'NL', '0655554444', 'NL99RABO0987654321', 'admin'), -- HIER STOND EEN ; MAAR MOET EEN , ZIJN
('roland@test.com', 'scrypt:32768:8:1$PVPeyts6gAQ5xt2l$65ea77454c6b60d43ac87bf8005d3ad4fb4885cc0d2bd60ba0c15ef4992d75c6cd9dae593e51f6c7233745d5737b0dc77807509857b95ae4908347cb6855a89e', 'Roland', '', 'twee', 'lindelaan 10', '3522 CR', 'NL', '0612345689', 'NL91ABNA0417164302', 'admin'); -- HIER MOET DE ;


INSERT INTO EVBOXLocations (locationName, address, city)
VALUES
('Utrecht Centraal', 'Stationsplein 1', 'Utrecht'),
('Bedrijventerrein West', 'Industrieweg 15', 'Amsterdam'),
('Winkelcentrum Zuid', 'Plein 5', 'Eindhoven');

INSERT INTO EVBoxes (locationID, serialNumber, softwareVersion)
VALUES
(1, '1231456745', 'v2.1.0'),
(2, '2231456745', 'v2.0.5'),
(3, '3231456745', 'v1.9.8');

INSERT INTO userCards (userID, cardUID, isActive)
VALUES
(1, '04BA2A2ADA1790', 1),
(2, '0497147A5B1994', 1),
(3, '04D5C8F1E3A201', 0);

INSERT INTO electricityPrice (logTime, price)
VALUES
('2025-10-07 10:00:00', 0.2850),
('2025-10-08 10:00:00', 0.3125),
('2025-10-09 10:00:00', 0.2990);

INSERT INTO chargeSessions (sessionID, cardUID, EVBOXID, locationName, sessionStart, sessionEnd, energyUsage, totalCost, status, createdAt, updatedAt)
VALUES
(1, '04BA2A2ADA1790', 1, 'Culemborg', '2025-10-07 11:30:00', '2025-10-07 14:00:00', 15.75, 5.06, 'completed', '2026-02-24 08:34:33', '2026-03-05 12:47:02'),
(2, '0497147A5B1994', 2, 'Utrecht', '2025-10-08 12:00:00', '2025-10-08 13:45:00', 10.50, 3.28, 'completed', '2026-02-24 08:34:33', '2026-03-05 12:47:24'),
(3, '04BA2A2ADA1790', 1, 'Amsterdam', '2025-10-08 13:00:00', NULL, NULL, NULL, 'active', '2026-02-24 08:34:33', '2026-03-05 12:47:31'),
(4, '04BA2A2ADA1790', 1, '', '2026-02-26 10:08:47', NULL, NULL, NULL, 'active', '2026-02-26 10:08:47', '2026-02-26 10:08:47');

