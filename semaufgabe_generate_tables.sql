-- Löscht alle Tabellen, falls sie existieren.
PRAGMA foreign_keys=off;
DROP TABLE IF EXISTS `House`;
DROP TABLE IF EXISTS `Address`;
DROP TABLE IF EXISTS `Zipcode`;
DROP TABLE IF EXISTS `State`;
DROP TABLE IF EXISTS `Country`;
DROP TABLE IF EXISTS `Coordinates`;
DROP TABLE IF EXISTS `Price`;
DROP TABLE IF EXISTS `City`;
DROP TABLE IF EXISTS `Properties`;
DROP TABLE IF EXISTS `LivingArea`;
DROP TABLE IF EXISTS `LotAreaUnit`;
DROP TABLE IF EXISTS `HomeType`;
DROP TABLE IF EXISTS `Currency`;
DROP TABLE IF EXISTS `Event`;
DROP TABLE IF EXISTS `County`;
DROP TABLE IF EXISTS `Offer`;
PRAGMA foreign_keys=on;

-- Erstellt die Tabelle City
CREATE TABLE `City` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `City` VARCHAR(50) NOT NULL
);

-- Erstellt die Tabelle Zipcode
CREATE TABLE `Zipcode` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Zipcode` INTEGER NOT NULL
);

-- Erstellt die Tabelle Coordinates
CREATE TABLE `Coordinates` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Longitude` FLOAT NOT NULL,
    `Latitude` FLOAT NOT NULL,
    `HasBadGeoCoordinates` BOOLEAN NOT NULL
);

-- Erstellt die Tabelle Country
CREATE TABLE `Country` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Country` VARCHAR(25) NOT NULL
);

-- Erstellt die Tabelle County
CREATE TABLE 'County' (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `County` VARCHAR(30) NOT NULL
);

-- Erstellt die Tabelle State mit entsprechenden Foreign Key
CREATE TABLE `State` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `State` VARCHAR(50) NOT NULL,
    `FK_Country` INTEGER NOT NULL,
    FOREIGN KEY ('FK_Country') REFERENCES Country (ID)
);

-- Erstellt die Tabelle Address mit entsprechenden Foreign Keys
CREATE TABLE `Address` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Address` VARCHAR(100) NOT NULL,
    `FK_City` INTEGER NOT NULL,
    `FK_State` INTEGER NOT NULL,
    `FK_Zipcode` INTEGER,
    `FK_Coordinates` INTEGER NOT NULL,
    `FK_County`INTEGER NOT NULL,
    FOREIGN KEY ('FK_City') REFERENCES City (ID),
    FOREIGN KEY ('FK_State') REFERENCES State (ID),
    FOREIGN KEY ('FK_Zipcode') REFERENCES Zipcode (ID),
    FOREIGN KEY ('FK_Coordinates') REFERENCES Coordinates (ID),
    FOREIGN KEY ('FK_County') REFERENCES County (ID)
);

-- Erstellt die Tabelle Currency
CREATE TABLE `Currency` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Currency` VARCHAR(5) NOT NULL
);

-- Erstellt die Tabelle State mit entsprechenden Foreign Key
CREATE TABLE `Price` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Price` VARCHAR(20) NOT NULL,
    `FK_Currency` INTEGER NOT NULL,
    FOREIGN KEY ('FK_Currency') REFERENCES Currency (ID)
);

-- Erstellt die Tabelle LotAreaUnit
CREATE TABLE `LotAreaUnit` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `LotAreaUnit` VARCHAR(5) NOT NULL
);

-- Erstellt die Tabelle LivingArea mit entsprechendem Foreign Key
CREATE TABLE `LivingArea` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `LivingArea` INTEGER NOT NULL,
    `LivingAreaValue` INTEGER NOT NULL,
    `FK_LotAreaUnit` INTEGER NOT NULL,
    FOREIGN KEY ('FK_LotAreaUnit') REFERENCES LotAreaUnit (ID)
);

-- Erstellt die Tabelle HomeType
CREATE TABLE `HomeType` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `HomeType` VARCHAR(15) NOT NULL
);

-- Erstellt die Tabelle Event
CREATE TABLE `Event` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Event` VARCHAR(15) NOT NULL
);

-- Erstellt die Tabelle Properties mit entsprechenden Foreign Keys
CREATE TABLE `Properties` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Bathrooms` INTEGER NOT NULL,
    `Bedrooms` INTEGER NOT NULL,
    `Buildingarea` INTEGER NOT NULL,
    `Parking` BOOLEAN NOT NULL,
    `HasGarage` BOOLEAN NOT NULL,
    `Garagespaces` INTEGER NOT NULL,
    `Levels` VARCHAR(30) NOT NULL,
    `Pool` BOOLEAN NOT NULL,
    `Spa` BOOLEAN NOT NULL,
    `IsNewConstruction` BOOLEAN NOT NULL,
    `HasPetsAllowed` BOOLEAN NOT NULL,
    `PricePerSquareFoot` VARCHAR(10),
    `YearBuilt` VARCHAR(4) NOT NULL,
    'IsForAuction' BOOLEAN NOT NULL,
    'IsBankOwned' BOOLEAN NOT NULL,
    'DatePosted' VARCHAR(20),
    `FK_HomeType` INTEGER NOT NULL,
    'FK_Event' INTEGER NOT NULL,
    FOREIGN KEY ('FK_HomeType') REFERENCES HomeType (ID),
    FOREIGN KEY ('FK_Event') REFERENCES Event (ID)
);

-- Erstellt die Tabelle House mit entsprechenden Foreign Keys
CREATE TABLE `House` (
    `ID` VARCHAR(40) NOT NULL,
    `Description` VARCHAR(10000),
    `FK_Price` INTEGER NOT NULL,
    `FK_Address` INTEGER NOT NULL,
    `FK_Properties` INTEGER NOT NULL,
    `FK_LivingArea` INTEGER NOT NULL,
    PRIMARY KEY (`ID`),
    FOREIGN KEY ('FK_Price') REFERENCES Price (ID),
    FOREIGN KEY ('FK_Address') REFERENCES Address (ID),
    FOREIGN KEY ('FK_Properties') REFERENCES Properties (ID),
    FOREIGN KEY ('FK_LivingArea') REFERENCES LivingArea (ID)
);

-- Erstellt die Tabelle Offer mit entsprechenden Foreign Keys
CREATE TABLE `Offer` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Offer` INTEGER NOT NULL,
    `BidderName` VARCHAR(50) NOT NULL,
    `FK_House` VARCHAR(40) NOT NULL,
    FOREIGN KEY ('FK_House') REFERENCES House (ID)
);