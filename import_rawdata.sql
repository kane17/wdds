SELECT * FROM 'RealEstate_California-adapted-new';

INSERT INTO Country ('Country')  SELECT DISTINCT country FROM 'RealEstate_California-adapted-new';
SELECT * FROM Country;

INSERT INTO Zipcode ('Zipcode')  SELECT DISTINCT zipcode FROM 'RealEstate_California-adapted-new' WHERE zipcode != '';
SELECT * FROM Zipcode;

-- TODO
INSERT INTO State (State, FK_Country) SELECT DISTINCT csv.state, c.ID FROM 'RealEstate_California-adapted-new' as csv, Country as c WHERE csv.state != '';
SELECT * FROM State;

INSERT INTO City ('City')  SELECT DISTINCT city FROM 'RealEstate_California-adapted-new' WHERE city != '';
SELECT * FROM City;

INSERT INTO County ('County')  SELECT DISTINCT county FROM 'RealEstate_California-adapted-new' WHERE county != '';
SELECT * FROM County;

INSERT INTO Coordinates ('Longitude', 'Latitude', 'HasBadGeoCoordinates') SELECT DISTINCT longitude, latitude, hasBadGeocode FROM 'RealEstate_California-adapted-new';
SELECT * FROM Coordinates;


INSERT INTO Address ('Address', 'FK_City', 'FK_State', 'FK_Zipcode', 'FK_Coordinates', 'FK_County')
SELECT csv.streetAddress, c.ID, s.ID, z.ID, coor.ID, cou.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN City c ON c.City = csv.city
     LEFT JOIN State s ON s.State = csv.state
     LEFT JOIN Zipcode z ON z.Zipcode = csv.zipcode
     LEFT JOIN Coordinates coor ON coor.Longitude = csv.longitude
        AND coor.Latitude = csv.latitude AND coor.HasBadGeoCoordinates = csv.hasBadGeocode
     LEFT JOIN County cou ON cou.County = csv.county;
SELECT * FROM Address;

INSERT INTO HomeType ('HomeType')  SELECT DISTINCT homeType FROM 'RealEstate_California-adapted-new' WHERE homeType != '';
SELECT * FROM HomeType;

INSERT INTO Event ('Event')  SELECT DISTINCT event FROM 'RealEstate_California-adapted-new' WHERE event != '';
SELECT * FROM Event;

INSERT INTO Currency ('Currency')  SELECT DISTINCT currency FROM 'RealEstate_California-adapted-new' WHERE currency != '';
SELECT * FROM Currency;

INSERT INTO LotAreaUnit ('LotAreaUnit')  SELECT DISTINCT lotAreaUnits FROM 'RealEstate_California-adapted-new' WHERE lotAreaUnits != '';
SELECT * FROM LotAreaUnit;


INSERT INTO Price ('Price', 'FK_Currency')
SELECT DISTINCT csv.price, c.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN Currency c ON c.Currency = csv.currency;
SELECT * FROM Price;




INSERT INTO LivingArea ('LivingArea', 'LivingAreaValue', 'FK_LotAreaUnit')
SELECT DISTINCT csv.livingArea, csv.livingAreaValue, l.ID FROM 'RealEstate_California-adapted-new' as csv
     LEFT JOIN LotAreaUnit l ON l.LotAreaUnit = csv.lotAraUnits;
SELECT * FROM LivingArea;


INSERT INTO Properties ('Bathrooms', 'Bedrooms', 'Buildingarea', 'Parking', 'HasGarage', 'Garagespaces', 'Levels', 'Pool',
                        'Spa', 'IsNewConstruction', 'HasPetsAllowed', 'PricePerSquareFoot', 'YearBuilt', 'IsForAuction',
                        'IsBankOwned', 'DatePosted', 'FK_HomeType', 'FK_Event')
SELECT DISTINCT csv.bathrooms, csv.bedrooms, csv.buildingArea, csv.parking, csv.hasGarage, csv.garageSpaces, csv.levels,
                csv.pool, csv.spa, csv.isNewConstruction, csv.hasPetsAllowed, csv.pricePerSquareFoot, csv.yearBuilt, csv.is_ForAuction,
                csv.is_BankOwned, csv.datePostedString, h.ID, e.ID FROM 'RealEstate_California-adapted-new' as csv
    LEFT JOIN HomeType h ON h.HomeType = csv.homeType
    LEFT JOIN Event e ON e.Event = csv.event;
SELECT * FROM Properties;


INSERT INTO House (ID, Description, FK_Price, FK_Address, FK_Properties, FK_LivingArea)
SELECT DISTINCT csv.id, csv.description, p.ID, a.ID, p.ID, l.ID,  FROM 'RealEstate_California-adapted-new' as csv
        LEFT JOIN HomeType h ON h.HomeType = csv.homeType
        LEFT JOIN Event e ON e.Event = csv.event;




