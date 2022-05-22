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
PRAGMA foreign_keys=on;

CREATE TABLE `City` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `City` VARCHAR(50) NOT NULL
);

CREATE TABLE `Zipcode` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Zipcode` INTEGER NOT NULL
);

CREATE TABLE `Coordinates` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Longitude` FLOAT NOT NULL,
    `Latitude` FLOAT NOT NULL,
    `HasBadGeoCoordinates` BOOL NOT NULL
);

CREATE TABLE `Country` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Country` VARCHAR(25) NOT NULL
);

CREATE TABLE 'County' (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `County` VARCHAR(30) NOT NULL
);

CREATE TABLE `State` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `State` VARCHAR(50) NOT NULL,
    `FK_Country` INTEGER NOT NULL,
    FOREIGN KEY ('FK_Country') REFERENCES Country (ID)
);

CREATE TABLE `Address` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Address` VARCHAR(100) NOT NULL,
    `FK_City` INTEGER NOT NULL,
    `FK_State` INTEGER NOT NULL,
    `FK_Zipcode` INTEGER NOT NULL,
    `FK_Coordinates` INTEGER NOT NULL,
    `FK_County`INTEGER NOT NULL,
    FOREIGN KEY ('FK_City') REFERENCES City (ID),
    FOREIGN KEY ('FK_State') REFERENCES State (ID),
    FOREIGN KEY ('FK_Zipcode') REFERENCES Zipcode (ID),
    FOREIGN KEY ('FK_Coordinates') REFERENCES Coordinates (ID),
    FOREIGN KEY ('FK_County') REFERENCES County (ID)
);

CREATE TABLE `Currency` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Currency` VARCHAR(5) NOT NULL
);

CREATE TABLE `Price` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Price` FLOAT NOT NULL,
    `FK_Currency` INTEGER NOT NULL,
    FOREIGN KEY ('FK_Currency') REFERENCES Currency (ID)
);

CREATE TABLE `LotAreaUnit` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `LotAreaUnit` VARCHAR(5) NOT NULL
);

CREATE TABLE `LivingArea` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `LivingArea` INTEGER NOT NULL,
    `LivingAreaValue` INTEGER NOT NULL,
    `FK_LotAreaUnit` INTEGER NOT NULL,
    FOREIGN KEY ('FK_LotAreaUnit') REFERENCES LotAreaUnit (ID)
);

CREATE TABLE `HomeType` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `HomeType` VARCHAR(15) NOT NULL
);

CREATE TABLE `Event` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Event` VARCHAR(15) NOT NULL
);

CREATE TABLE `Properties` (
    `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Bathrooms` INTEGER NOT NULL,
    `Bedrooms` INTEGER NOT NULL,
    `Buildingarea` INTEGER NOT NULL,
    `Parking` BOOL NOT NULL,
    `HasGarage` BOOL NOT NULL,
    `Garagespaces` INTEGER NOT NULL,
    `Levels` VARCHAR(10) NOT NULL,
    `Pool` BOOL NOT NULL,
    `Spa` BOOL NOT NULL,
    `IsNewConstruction` BOOL NOT NULL,
    `HasPetsAllowed` BOOL NOT NULL,
    `PricePerSquareFoot` VARCHAR(10) NOT NULL,
    `YearBuilt` VARCHAR(10) NOT NULL,
    'IsForAuction' BOOL NOT NULL,
    'IsBankOwned' BOOL NOT NULL,
    'DatePosted' VARCHAR(20) NOT NULL,
    `FK_HomeType` INTEGER NOT NULL,
    'FK_Event' INTEGER NOT NULL,
    FOREIGN KEY ('FK_HomeType') REFERENCES HomeType (ID),
    FOREIGN KEY ('FK_Event') REFERENCES Event (ID)
);


CREATE TABLE `House` (
    `ID` INTEGER NOT NULL,
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


SELECT * FROM  `House`;
SELECT * FROM  `Address`;
SELECT * FROM  `Zipcode`;
SELECT * FROM  `State`;
SELECT * FROM  `Country`;
SELECT * FROM  `Coordinates`;
SELECT * FROM  `Price`;
SELECT * FROM  `City`;
SELECT * FROM  `Properties`;
SELECT * FROM  `LivingArea`;
SELECT * FROM  `LotAreaUnit`;
SELECT * FROM  `HomeType`;
SELECT * FROM  `Currency`;
SELECT * FROM  `Event`;
SELECT * FROM  `County`;