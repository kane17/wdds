SELECT * FROM House WHERE (SELECT ID FROM Properties WHERE YearBuilt = '2020' OR YearBuilt = '2021' OR YearBuilt = '2022' OR YearBuilt = '9999')

-- Aufgabe 1

DROP VIEW Houses;
CREATE VIEW IF NOT EXISTS Houses (ID, Country, datePosted, IsBankOwnded, IsForAuction,
    Event, Price, PricePerSquareFoot, City, State, YearBuilt, Address, Zipcode, Longitude, Latitude,
    HasBadGeocode, Description, Currency, LivingArea, LivingAreaValue, LotAreaUnit, Bathrooms, Bedrooms,
    BuildingArea, Parking, GarageSpaces, HasGarage, Levels, Pool, Spa, IsNewConstruction, HasPetsAllowed,
    HomeType, County) AS SELECT h.ID, country.Country, prop.datePosted, prop.IsBankOwnded, prop.IsForAuction,
    e.Event, pr.Price, prop.PricePerSquareFoot, c.City, s.State, prop.YearBuilt, a.Address, z.Zipcode, co.Longitude,
    co.Latitude, co.HasBadGeocode, prop.Description, cur.Currency, li.LivingArea, li.LivingAreaValue, lot.LotAreaUnit,
    prop.Bathrooms, prop.Bedrooms, prop.Buildingarea, prop.Parking, prop.Garagespaces, prop.HasGarage, prop.Levels,
    prop.Pool, prop.Spa, prop.IsNewConstruction, prop.HasPetsAllowed FROM House h
    INNER JOIN Price pr ON pr.ID = h.FK_Price
    INNER JOIN Currency cur ON cur.ID = pr.FK_Currency
    INNER JOIN Address a ON a.ID = h.FK_Address
    INNER JOIN City c ON c.ID = a.FK_City
    INNER JOIN State s ON s.ID = a.FK_State
    INNER JOIN Country country ON Country.ID = s.FK_Country
    INNER JOIN Zipcode z ON a.FK_Zipcode = z.ID
    INNER JOIN Coordinates co ON a.FK_Coordinates = co.ID
    INNER JOIN County cou ON a.FK_County = cou.ID
    INNER JOIN LivingArea li ON li.ID = h.FK_LivingArea
    INNER JOIN LotAreaUnit lot ON lot.ID = li.FK_LotAreaUnit
    INNER JOIN Properties prop ON prop.ID = h.FK_Properties
    INNER JOIN Event e ON e.ID = prop.FK_Event
    INNER JOIN HomeType ho ON ho.ID = prop.FK_HomeType;


CREATE VIEW HouseView FROM House;









h.ID, country.Country, prop.datePosted, prop.IsBankOwnded, prop.IsForAuction,
    e.Event, pr.Price, prop.PricePerSquareFoot, c.City, s.State, prop.YearBuilt, a.Address, z.Zipcode, co.Longitude, co.Latitude,
    co.HasBadGeocode, prop.Description, cur.Currency, li.LivingArea, li.LivingAreaValue, lot.LotAreaUnit, prop.Bathrooms, prop.Bedrooms,
    BuildingArea, Parking, GarageSpaces, HasGarage, Levels, Pool, Spa, IsNewConstruction, HasPetsAllowed,

-- Aufgabe 2
SELECT count(*) as 'Anzahl Häuser mit Baujahr 2020 und höher' FROM House WHERE FK_Properties IN (SELECT ID From Properties WHERE YearBuilt = '2020' OR YearBuilt = '2021' OR YearBuilt = '2022' OR YearBuilt = '9999');


-- Aufgabe 3
SELECT DISTINCT c.City FROM City c
                                INNER JOIN Address a ON a.FK_City = c.ID
                                INNER JOIN County co ON co.ID = a.FK_County
WHERE  ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1)



















SELECT c.City FROM City c
    INNER JOIN Address a ON a.FK_City = c.ID
    INNER JOIN County co ON co.ID = a.FK_County
    WHERE (SELECT COUNT(*) FROM Address WHERE Address.FK_County > 1)

SELECT c.City FROM City c
   INNER JOIN Address a ON a.FK_City = c.ID
   INNER JOIN County co ON co.ID = a.FK_County GROUP BY a.FK_COUNTY


SELECT * FROM Address a
    INNER JOIN County co ON co.ID = a.FK_County
    INNER JOIN City c ON c.ID = a.FK_City;


SELECT * FROM Address a
    INNER JOIN County co ON co.ID = a.FK_County
    INNER JOIN City c ON c.ID = a.FK_City;






SELECT c.City, co.County, a.FK_City, a.FK_County FROM City c
                                                          INNER JOIN Address a ON a.FK_City = c.ID
                                                          INNER JOIN County co ON co.ID = a.FK_County
WHERE  (SELECT DISTINCT Address.FK_County FROM Address WHERE Address.FK_City=c.ID) > 1


SELECT c.City, co.County, a.FK_City, a.FK_County FROM Address a
                                                          INNER JOIN City c ON a.FK_City = c.ID
                                                          INNER JOIN County co ON co.ID = a.FK_County
WHERE c.ID IN  (SELECT DISTINCT Address.FK_County FROM Address WHERE Address.FK_City=c.ID)

-- Hier sieht man beide FK
SELECT DISTINCT Address.FK_County FROM Address WHERE Address.FK_City=481

SELECT * FROM City WHERE City.City = 'Fiddletown';

-- KÖNNTE DIE LÖSUNG SEIN:

SELECT c.City, co.County, a.FK_City, a.FK_County FROM City c
                                                          INNER JOIN Address a ON a.FK_City = c.ID
                                                          INNER JOIN County co ON co.ID = a.FK_County
WHERE  (SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1)





SELECT * FROM City;


    WHERE a.FK_City IN (SELECT ad.FK_City FROM Address ad WHERE (SELECT COUNT(*) FROM Address WHERE Address.FK_County = ad.FK_County) > 1);

    SELECT a.ID, a.Address, City, State, Zipcode, Longitude, Latitude, County FROM Address  a
    INNER JOIN City  c ON c.ID  = a.FK_City
    INNER JOIN State s ON s.ID = a.FK_State
    INNER JOIN Zipcode z ON a.FK_Zipcode = z.ID
    INNER JOIN Coordinates co ON a.FK_Coordinates = co.ID
    INNER JOIN County cou ON a.FK_County = cou.ID
WHERE a.ID = 21750;


SELECT City FROM City WHERE FK