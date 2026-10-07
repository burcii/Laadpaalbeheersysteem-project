# **Database Schema Changelog**
## 1. General Schema & Integrity Changes
| Change Type        | Description                                                                                  | Rationale                                                                                 |
|:-------------------|:---------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------|
| **Clean Rebuild**  | Added DROP TABLE IF EXISTS for all tables at the start of the script.                        | Ensures a clean slate. **Note: This deletes all existing data.**                          |
| **Data Integrity** | **Added explicit FOREIGN KEY constraints** to EVBoxes, userCards, and chargeSessions.        | Crucial for data integrity. Enforces relationships between tables.                        |
| **Auditing**       | Added createdAt and updatedAt columns to users, EVBOXLocations, EVBoxes, and chargeSessions. | Standard practice for tracking when records were created and last modified (audit trail). |
| **Performance**    | Added explicit CREATE INDEX statements for key lookup fields.                                | Improves application query speed for history lookups and active session checks.           |
| **Sample Data**    | Sample data structure and values were completely replaced.                                   | Updated to reflect the new column names and data types.                                   |

## **2. Table Specific Changes**
### **1. users Table**
| Column                | Old Structure        | New Structure                                | Change Type                                                                                   |
|:----------------------|:---------------------|:---------------------------------------------|:----------------------------------------------------------------------------------------------|
| **tussenvoegsel**     | VARCHAR(10) NOT NULL | **nameParticle** VARCHAR(10) DEFAULT ''      | **RENAME.** Changed to an English term for better international clarity. Default value added. |
| email                 | VARCHAR(50)          | VARCHAR(100)                                 | Size increased.                                                                               |
| adress                | VARCHAR(50)          | VARCHAR(100)                                 | Size increased.                                                                               |
| zipcode               | VARCHAR(8)           | VARCHAR(10)                                  | Size increased.                                                                               |
| phonenumber           | INT NOT NULL         | VARCHAR(20) NOT NULL                         | **Data Type Change.** Better for storing non-numeric phone formats.                           |
| bankaccount           | VARCHAR(25)          | VARCHAR(34)                                  | Size increased (accommodates longer IBAN formats).                                            |
| role                  | INT NOT NULL         | ENUM('user', 'admin', 'management') NOT NULL | **Data Type Change.** Restricts values to defined roles.                                      |
| createdAt / updatedAt | *(Not present)*      | DATETIME NOT NULL                            | **NEW Columns.**                                                                              |

### **2. locations -> EVBOXLocations Table**
| Column         | Old Structure (locations) | New Structure (EVBOXLocations) | Change Type                                              |
|:---------------|:--------------------------|:-------------------------------|:---------------------------------------------------------|
| **Table Name** | locations                 | **EVBOXLocations**             | **RENAME.** Clearly links locations to the EVBox system. |
| locationName   | VARCHAR(20)               | VARCHAR(50)                    | Size increased.                                          |
| address / city | *(Not present)*           | VARCHAR(100) / VARCHAR(50)     | **NEW Columns.** Added physical address fields.          |
| createdAt      | *(Not present)*           | DATETIME NOT NULL              | **NEW Column.**                                          |

### **3. EVBoxes Table**
| Column          | Old Structure   | New Structure                                      | Change Type                                                                   |
|:----------------|:----------------|:---------------------------------------------------|:------------------------------------------------------------------------------|
| isUsed          | TINYINT(1)      | *(Removed)*                                        | **Removed Column.** Usage status is now tracked via the chargeSessions table. |
| softwareVersion | INT NOT NULL    | VARCHAR(20) NOT NULL                               | **Data Type Change.** Better for storing version strings (e.g., "v2.1.0").    |
| maxPowerKW      | *(Not present)* | DECIMAL(5,2)                                       | **NEW Column.** Added to track the maximum output power of the unit.          |
| **Foreign Key** | *(Implicit)*    | FOREIGN KEY (locationID) REFERENCES EVBOXLocations | **NEW Constraint.** Updated to reference the new location table name.         |

### 4. userPas -> userCards Table
| Column          | Old Structure (userPas) | New Structure (userCards)           | Change Type                                                              |
|:----------------|:------------------------|:------------------------------------|:-------------------------------------------------------------------------|
| **Table Name**  | userPas                 | **userCards**                       | **RENAME.** More descriptive name for the physical pass/card.            |
| **Primary Key** | passNumber (PK)         | **cardID** (New PK, AUTO_INCREMENT) | **Structural Change.** Moves PK to a simpler integer ID.                 |
| **passNumber**  | VARCHAR(25) (PK)        | **cardUID** VARCHAR(25) UNIQUE      | **RENAME/Constraint Change.** More descriptive name for the RFID number. |
| isActive        | *(Not present)*         | TINYINT(1) DEFAULT 1                | **NEW Column.** Allows temporary deactivation of a card.                 |

### **5. electricityPrice Table**
| Column           | Old Structure   | New Structure                       | Change Type                                                      |
|:-----------------|:----------------|:------------------------------------|:-----------------------------------------------------------------|
| priceID          | *(Not present)* | INT PRIMARY KEY AUTO_INCREMENT      | **NEW Primary Key.**                                             |
| price            | DECIMAL(4,2)    | DECIMAL(10,4)                       | **Data Type Change.** Increased precision for financial logging. |
| **Unique Index** | *(Not present)* | UNIQUE KEY unique_logtime (logTime) | **NEW Constraint.**                                              |

### **6. chargeSessions Table**
| Column          | Old Structure     | New Structure                                        | Change Type                                                                                  |
|:----------------|:------------------|:-----------------------------------------------------|:---------------------------------------------------------------------------------------------|
| **passNumber**  | INT NOT NULL      | **cardUID** VARCHAR(25) NOT NULL                     | **RENAME/Type Change.** Consistent name for the foreign key, now links to userCards.cardUID. |
| **EVBOXNumber** | INT NOT NULL      | **EVBOXID** INT NOT NULL                             | **RENAME.** Consistent name for the foreign key, matches EVBoxes.EVBOXID.                    |
| sessionEnd      | DATETIME NOT NULL | DATETIME NULL                                        | **Nullable.** Allows the session record to be inserted while charging is active.             |
| energyUsage     | INT NOT NULL      | DECIMAL(10,2) NULL                                   | **Data Type Change.** Allows decimal usage values and is nullable.                           |
| totalCost       | *(Not present)*   | DECIMAL(10,2) NULL                                   | **NEW Column.** Added for calculated billing cost.                                           |
| status          | *(Not present)*   | ENUM('active', 'completed', 'failed', 'interrupted') | **NEW Column.** Added to track the current state of a charging session.                      |
| **Indexes**     | *(Implicit)*      | idx_sessions_active and idx_sessions_user            | **Update.** Explicit indexes added with consistent column names.                             |