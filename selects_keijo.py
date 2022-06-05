import sqlite3

# Datenbankverbindung herstellen
database = sqlite3.connect('../wdda_sem_db1.db')
cursor = database.cursor()


# Aufgabe 2
def get_amount_of_buildings_built_after(yearbuilt):
    # TODO: query funktioniert so nicht
    sqlquery = "SELECT count(*) FROM House WHERE FK_Properties IN (SELECT ID From Properties WHERE YearBuilt >= ?);"
    result = cursor.execute(sqlquery, (yearbuilt,))
    amount = result.fetchone()
    print("Anzahl Häuser mit Baujahr ", yearbuilt, " und höher (inkl. Jahr 9999): ", amount[0])


#get_amount_of_buildings_built_after('1000000')


#Aufgabe 3
# sqlquery = "SELECT DISTINCT c.City FROM City c INNER JOIN Address a ON a.FK_City = c.ID INNER JOIN County co ON co.ID = a.FK_County WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1)"
# result = cursor.execute(sqlquery)
# cities = result.fetchall()
# print("Städte, mit Immobilien in mehr als einem Landkreis: ")
# for city in cities:
#     print(city[0])
#
# cursor.close()
# def get_amount_of_cities_with_more_than_one_house():
#     sqlquery = "SELECT DISTINCT c.City FROM City c " \
#                "INNER JOIN Address a ON a.FK_City = c.ID " \
#                "INNER JOIN County co ON co.ID = a.FK_County " \
#                "WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1);"
#     result = cursor.execute(sqlquery)
#     summarycities = result.fetchall()
#     print("Städte, mit Immobilien in mehr als einem Landkreis:")
#     for x in summarycities:
#         print(x)
#
# get_amount_of_cities_with_more_than_one_house()


# Aufgabe 4
def select_cities_by_avg_price():
    sqlquery = """SELECT c.City, ROUND(AVG(p.Price), 2) AS 'Durchschnittlicher Preis' FROM House h
    LEFT JOIN Address a ON a.ID = h.FK_Address
    LEFT JOIN Price p ON h.FK_Price = p.ID
    LEFT JOIN City c ON c.ID = a.FK_City GROUP BY c.City ORDER BY ROUND(AVG(p.Price), 2) DESC;"""

    result = cursor.execute(sqlquery)

    for entry in result.fetchall():
        print(entry)

select_cities_by_avg_price()


# Aufgabe 5
def select_cities_with_sqftprices_over_average():
    sqlquery = """SELECT c.City, ROUND(AVG(prop.PricePerSquareFoot), 2) AS PricePerSquareFoot FROM House h
        LEFT JOIN Address a ON a.ID = h.FK_Address
        LEFT JOIN City c ON c.ID = a.FK_City
        LEFT JOIN Properties prop ON prop.ID = h.FK_Properties
    WHERE CAST(PricePerSquareFoot AS FLOAT) > CAST((SELECT ROUND(AVG(prop.PricePerSquareFoot), 2) AS 'Preis Pro Quadratmeter'
    FROM House h LEFT JOIN Properties prop ON prop.ID = h.FK_Properties WHERE prop.PricePerSquareFoot != 'N/A') AS FLOAT) GROUP BY c.City;"""

    result = cursor.execute(sqlquery)

    print("{:<28} {:<35}".format('City', 'Price per SquareFoot'))
    for entry in result.fetchall():
        city, pricePerSquareFoot = entry
        print("{:<28} {:<35}".format(city, pricePerSquareFoot))


# select_cities_with_sqftprices_over_average()


# Aufgabe 6
def select_offers_for_city(city):
    sqlquery = """SELECT HT.HomeType, P2.Price, h.Description  FROM City c
        LEFT JOIN Address a ON a.FK_City = c.ID
        LEFT JOIN House h ON h.FK_Address = a.ID
        LEFT JOIN Properties P on h.FK_Properties = P.ID
        LEFT JOIN HomeType HT on P.FK_HomeType = HT.ID
        LEFT JOIN Event E on P.FK_Event = E.ID
        LEFT JOIN Price P2 on h.FK_Price = P2.ID
    WHERE c.City = ? AND E.Event = 'Listed for sale';"""

    result = cursor.execute(sqlquery, (city,))

    for entry in result.fetchall():
        print(entry)



city = input('Aufgabe 6: Geben Sie bitte eine Stadt ein')
select_offers_for_city(city)