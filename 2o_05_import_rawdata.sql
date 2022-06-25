-- Als erstes müssen wir sicherstellen, dass das CSV File bereits in eine Tabelle importiert wurde.
SELECT * FROM 'RealEstate_California-adapted-new';

-- Hier werden diejenigen Tabellen abgefüllt, welche keine Abhängigkeiten haben, also keine Foreign Keys benötigen.
-- Dazu haben wir SELECT DISTINCT verwendet, da keine doppelten Einträge abgefüllt werden sollten.
-- Im statement werden auch die leeren Werte ignoriert um NOT NULL Constraint Violations zu vermeiden.
-- Abfüllen der Country Tabelle.
INSERT INTO Country ('Country')  SELECT DISTINCT country FROM 'RealEstate_California-adapted-new';
SELECT * FROM Country;

-- Abfüllen der Zipcode Tabelle.
INSERT INTO Zipcode ('Zipcode')  SELECT DISTINCT zipcode FROM 'RealEstate_California-adapted-new' WHERE zipcode != '';
SELECT * FROM Zipcode;

-- Abfüllen der State Tabelle.
INSERT INTO State (State, FK_Country) SELECT DISTINCT csv.state, c.ID FROM 'RealEstate_California-adapted-new' as csv, Country as c WHERE csv.state != '';
SELECT * FROM State;

-- Abfüllen der City Tabelle.
INSERT INTO City ('City')  SELECT DISTINCT city FROM 'RealEstate_California-adapted-new' WHERE city != '';
SELECT * FROM City;

-- Abfüllen der County Tabelle.
INSERT INTO County ('County')  SELECT DISTINCT county FROM 'RealEstate_California-adapted-new' WHERE county != '';
SELECT * FROM County;

-- Abfüllen der Coordinates Tabelle.
INSERT INTO Coordinates ('Longitude', 'Latitude', 'HasBadGeoCoordinates') SELECT DISTINCT longitude, latitude, hasBadGeocode FROM 'RealEstate_California-adapted-new';
SELECT * FROM Coordinates;

-- Hier werden die Addressdaten aller Häuser abgefüllt, dabei wird ein LEFT JOIN auf die oben abgefüllten Tabellen gemacht,
-- um die Foreign Keys korrekt aufzulösen.
INSERT INTO Address ('Address', 'FK_City', 'FK_State', 'FK_Zipcode', 'FK_Coordinates', 'FK_County')
SELECT csv.streetAddress, c.ID, s.ID, z.ID, coor.ID, cou.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN City c ON c.City = csv.city
     LEFT JOIN State s ON s.State = csv.state
     LEFT JOIN Zipcode z ON z.Zipcode = csv.zipcode
     LEFT JOIN Coordinates coor ON coor.Longitude = csv.longitude
        AND coor.Latitude = csv.latitude AND coor.HasBadGeoCoordinates = csv.hasBadGeocode
     LEFT JOIN County cou ON cou.County = csv.county;
SELECT * FROM Address;

-- Abfüllen der HomeType Tabelle.
INSERT INTO HomeType ('HomeType')  SELECT DISTINCT homeType FROM 'RealEstate_California-adapted-new' WHERE homeType != '';
SELECT * FROM HomeType;

-- Abfüllen der Event Tabelle.
INSERT INTO Event ('Event')  SELECT DISTINCT event FROM 'RealEstate_California-adapted-new' WHERE event != '';
SELECT * FROM Event;

-- Abfüllen der Currency Tabelle.
INSERT INTO Currency ('Currency')  SELECT DISTINCT currency FROM 'RealEstate_California-adapted-new' WHERE currency != '';
SELECT * FROM Currency;

-- Abfüllen der LotAreaUnit Tabelle.
INSERT INTO LotAreaUnit ('LotAreaUnit')  SELECT DISTINCT lotAreaUnits FROM 'RealEstate_California-adapted-new' WHERE lotAreaUnits != '';
SELECT * FROM LotAreaUnit;

-- Price wird mit Foreign Key Currency abgefüllt.
INSERT INTO Price ('Price', 'FK_Currency')
SELECT DISTINCT csv.price, c.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN Currency c ON c.Currency = csv.currency;
SELECT * FROM Price;

-- Hier wird die LivingArea Tabelle importiert, mit Referenz auf die LotAreaUnit.
INSERT INTO LivingArea ('LivingArea', 'LivingAreaValue', 'FK_LotAreaUnit')
SELECT DISTINCT csv.livingArea, csv.livingAreaValue, l.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN LotAreaUnit l ON l.LotAreaUnit = csv.lotAreaUnits;
SELECT * FROM LivingArea;

-- Hier werden die Properties der einzelnen Häuser in eine eigene Tabelle geladen. Zusätzlich werden die Foreign Keys
-- HomeType und Event abgefragt.
INSERT INTO Properties ('Bathrooms', 'Bedrooms', 'Buildingarea', 'Parking', 'HasGarage', 'Garagespaces', 'Levels', 'Pool',
                        'Spa', 'IsNewConstruction', 'HasPetsAllowed', 'PricePerSquareFoot', 'YearBuilt', 'IsForAuction',
                        'IsBankOwned', 'DatePosted', 'FK_HomeType', 'FK_Event')
SELECT DISTINCT csv.bathrooms, csv.bedrooms, csv.buildingArea, csv.parking, csv.hasGarage, csv.garageSpaces, csv.levels,
                csv.pool, csv.spa, csv.isNewConstruction, csv.hasPetsAllowed, csv.pricePerSquareFoot, csv.yearBuilt, csv.is_ForAuction,
                csv.is_BankOwned, csv.datePostedString, h.ID, e.ID FROM 'RealEstate_California-adapted-new' as csv
    LEFT JOIN HomeType h ON h.HomeType = csv.homeType
    LEFT JOIN Event e ON e.Event = csv.event;
SELECT * FROM Properties;

-- Zum Schluss wird die zentrale HouseTabelle mit allen Referenzen abgefüllt.
-- Mit Hilfe von Sub Selects, stellen wir sicher, dass die korrekten Address und Properties Einträge referenziert werden.
INSERT INTO House (ID, Description, FK_Price, FK_Address, FK_Properties, FK_LivingArea)
SELECT csv.id, csv.description, p.ID, a.ID, prop.ID, l.ID  FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN Price p ON p.Price = csv.price
     LEFT JOIN Address a ON a.Address = csv.streetAddress
        AND a.FK_County = (SELECT ID FROM County WHERE County.County = csv.county)
        AND a.FK_Coordinates = (SELECT ID FROM Coordinates WHERE Coordinates.Latitude = csv.latitude
        AND Coordinates.Longitude = csv.longitude AND Coordinates.HasBadGeoCoordinates = csv.hasBadGeocode)
        AND a.FK_City = (SELECT ID FROM City WHERE City.City = csv.city)
        AND (a.FK_Zipcode = (SELECT ID FROM Zipcode WHERE Zipcode.Zipcode = csv.zipcode) OR csv.zipcode IS NULL)
    LEFT JOIN Properties prop on prop.Bathrooms = csv.bathrooms AND prop.Bedrooms = csv.bedrooms
        AND prop.Buildingarea = csv.buildingArea AND prop.Parking = csv.parking AND prop.HasGarage = csv.hasGarage
        AND prop.Garagespaces = csv.garageSpaces AND prop.Levels = csv.levels AND prop.Pool = csv.pool
        AND prop.Spa = csv.spa AND prop.IsNewConstruction = csv.isNewConstruction AND prop.HasPetsAllowed = csv.hasPetsAllowed
        AND prop.PricePerSquareFoot = csv.pricePerSquareFoot AND prop.YearBuilt = csv.yearBuilt
        AND prop.IsForAuction = csv.is_ForAuction AND prop.IsBankOwned = csv.is_BankOwned
        AND ((prop.DatePosted = csv.datePostedString) OR csv.datePostedString IS NULL)
        AND prop.FK_HomeType = (SELECT ID FROM HomeType WHERE HomeType.HomeType = csv.homeType)
        AND prop.FK_Event = (SELECT ID FROM Event WHERE Event.Event = csv.event)
    LEFT JOIN LivingArea l ON l.LivingArea = csv.livingArea AND l.LivingAreaValue = csv.livingAreaValue
        AND l.FK_LotAreaUnit = (SELECT ID FROM LotAreaUnit WHERE LotAreaUnit.LotAreaUnit = csv.lotAreaUnits) ;
SELECT * FROM House;


-- Zum Schluss werden einige Angebote in die Tabelle Offer geladen
INSERT INTO Offer (Offer, BidderName, FK_House) VALUES
(1500000, 'Elon Musk', '94502-24870550'),
(1910000, 'Bill Gates', '90008-20577035'),
(3550000, 'LeBron James', '90405-2070057452'),
(1200000, 'Stephen Curry', '94112-15170795'),
(599000, 'Michelle Obama', '95828-240358194');
SELECT * FROM Offer;
