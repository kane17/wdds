SELECT * FROM House WHERE (SELECT ID FROM Properties WHERE YearBuilt = '2020' OR YearBuilt = '2021' OR YearBuilt = '2022' OR YearBuilt = '9999')

-- Aufgabe 1

DROP VIEW Houses;
CREATE VIEW IF NOT EXISTS Houses AS
SELECT h.ID AS ID, country.Country AS Country, prop.DatePosted AS datePostedString, prop.IsBankOwned as is_bankOwned, prop.IsForAuction AS is_forAuction, e.Event AS event,
       pr.Price AS price, prop.PricePerSquareFoot AS pricePerSquareFoot, c.City AS city, s.State AS state, prop.YearBuilt AS yearBuilt, a.Address as streetAddress, z.Zipcode AS zipcode,
       co.Longitude AS longitude, co.Latitude AS latitude, co.HasBadGeoCoordinates AS hasBadGeocode, h.Description AS description, cur.Currency as currency, li.LivingArea AS livingArea,
       li.LivingAreaValue AS livingAreaValue, lot.LotAreaUnit AS lotAreaUnit, prop.Bathrooms AS bathrooms, prop.Bedrooms AS bedrooms, prop.Buildingarea AS buildingArea,
       prop.Parking AS parking, prop.Garagespaces AS garageSpaces, prop.HasGarage AS hasGarage, prop.Levels AS levels, prop.Pool AS pool, prop.Spa AS spa, prop.IsNewConstruction AS isNewConstruction,
       prop.HasPetsAllowed AS hasPetsAllowed, ho.HomeType AS homeType, cou.County AS county FROM House h
             LEFT  JOIN Price pr ON pr.ID = h.FK_Price
             LEFT  JOIN Currency cur ON cur.ID = pr.FK_Currency
             LEFT  JOIN Address a ON a.ID = h.FK_Address
             LEFT  JOIN City c ON c.ID = a.FK_City
             LEFT  JOIN State s ON s.ID = a.FK_State
             LEFT  JOIN Country country ON Country.ID = s.FK_Country
             LEFT  JOIN Zipcode z ON a.FK_Zipcode = z.ID
             LEFT  JOIN Coordinates co ON a.FK_Coordinates = co.ID
             LEFT  JOIN County cou ON a.FK_County = cou.ID
             LEFT  JOIN LivingArea li ON li.ID = h.FK_LivingArea
             LEFT  JOIN LotAreaUnit lot ON lot.ID = li.FK_LotAreaUnit
             LEFT  JOIN Properties prop ON prop.ID = h.FK_Properties
             LEFT  JOIN Event e ON e.ID = prop.FK_Event
             LEFT  JOIN HomeType ho ON ho.ID = prop.FK_HomeType;


-- Aufgabe 2
SELECT count(*) as 'Anzahl Häuser mit Baujahr 2020 und höher' FROM House WHERE FK_Properties IN (SELECT ID From Properties WHERE YearBuilt = '2020' OR YearBuilt = '2021' OR YearBuilt = '2022' OR YearBuilt = '9999');


-- Aufgabe 3 TODO: OPTIMIERE!
SELECT DISTINCT c.City FROM City c
                                INNER JOIN Address a ON a.FK_City = c.ID
                                INNER JOIN County co ON co.ID = a.FK_County
WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1)



-- Aufgabe 4 TODO
SELECT City, AVG(p.Price) AS 'Durchschnittlicher Preis' FROM Address a
             INNER JOIN House h ON a.ID = h.FK_Address
             INNER JOIN Price p ON h.FK_Price = p.ID
             INNER JOIN City c ON c.ID = a.FK_City GROUP BY City;



WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1) ORDER BY DESC;

SELECT avg(p.Price) AS avgPrice, c.City FROM House h
INNER JOIN Price p ON h.FK_Price = p.ID
INNER JOIN Address a ON a.ID = h.FK_Address
INNER JOIN City c ON c.ID = a.FK_City
WHERE (SELECT DISTINCT c.City FROM City) ORDER BY avgPrice DESC;










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