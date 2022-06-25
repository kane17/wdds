-- Aufgabe 1
-- Zunächst wir die View gelöscht, falls sie bereits existiert.
-- Im nächsten Schritt wird die View erstellt, mithilfe von LEFT JOIN auf alle Tabellen von unserem Schema.
-- Dabei werden immer die Foreign Keys mit den IDs verglichen um die Beziehung sauber aufzulösen.
DROP VIEW IF EXISTS Houses;
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
-- Mithilfe von count() und einem Sub-Select, welcher prüft ob das Baujahr 2021 oder 2022 ist, wurde Aufgabe 2 gelöst.
SELECT count(*) as 'Anzahl Häuser mit Baujahr 2020 und höher' FROM House WHERE FK_Properties IN (SELECT ID From Properties WHERE YearBuilt = '2021' OR YearBuilt = '2022');


-- Aufgabe 3
-- Mithilfe von INNER JOIN werden die Städte abgefragt, welche Immobilien in mehreren Counties haben.
-- Um die Anzahl counties zu vergleichen, haben wir wieder ein SELECT COUNT() verwendet im Sub-Select
SELECT DISTINCT c.City FROM City c
    INNER JOIN Address a ON a.FK_City = c.ID
    INNER JOIN County co ON co.ID = a.FK_County
WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1);



-- Aufgabe 4
-- Hier werden die Städte mit gerundetem durchschnittlichem Preis und nach Preis absteigend sortiert, angezeigt.
-- Der Durschnitt wird mit AVG() berechnet und gerundet wird mit ROUND()
SELECT c.City, ROUND(AVG(p.Price), 2) AS 'Durchschnittlicher Preis' FROM House h
    LEFT JOIN Address a ON a.ID = h.FK_Address
    LEFT JOIN Price p ON h.FK_Price = p.ID
    LEFT JOIN City c ON c.ID = a.FK_City GROUP BY c.City ORDER BY ROUND(AVG(p.Price), 2) DESC;


-- Aufgabe 5
-- Hier wird wie in Aufgabe 4 der Durchschnitt des Price pro Quadratfuss mit ROUND(AVG()) berechnet.
-- Da wir PricePerSquareFoot als VARCHAR in der Datenbank haben, muss ein CAST AS FLOAT gemacht werden, damit der Wert
-- sauber berechnet werden kann. Zusätzlich mussten die Werte 'N/A' von PricePerSquareFoot ignoriert werden um eine
-- fehlerfreie Berechnung zu ermöglichen. Zusätzlich wird jeweils noch der Name der Stadt ausgegeben.
SELECT c.City, ROUND(AVG(prop.PricePerSquareFoot), 2) AS PricePerSquareFoot FROM House h
    LEFT JOIN Address a ON a.ID = h.FK_Address
    LEFT JOIN City c ON c.ID = a.FK_City
    LEFT JOIN Properties prop ON prop.ID = h.FK_Properties
    WHERE CAST(PricePerSquareFoot AS FLOAT) > CAST((SELECT ROUND(AVG(prop.PricePerSquareFoot), 2) AS 'Preis Pro Quadratfuss'
    FROM House h LEFT JOIN Properties prop ON prop.ID = h.FK_Properties WHERE prop.PricePerSquareFoot != 'N/A') AS FLOAT) GROUP BY c.City;


-- Aufgabe 6
-- Hier werden alle Angebote der Stadt Parlier angezeigt, sprich diejenigen Einträge welche den Event 'Listed for sale'
-- hinterlegt haben.
SELECT HT.HomeType, P2.Price, h.Description  FROM City c
    LEFT JOIN Address a ON a.FK_City = c.ID
    LEFT JOIN House h ON h.FK_Address = a.ID
    LEFT JOIN Properties P on h.FK_Properties = P.ID
    LEFT JOIN HomeType HT on P.FK_HomeType = HT.ID
    LEFT JOIN Event E on P.FK_Event = E.ID
    LEFT JOIN Price P2 on h.FK_Price = P2.ID
WHERE c.City = 'Parlier' AND E.Event = 'Listed for sale';
