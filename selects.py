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


get_amount_of_buildings_built_after('1000000')


#Aufgabe 3
# sqlquery = "SELECT DISTINCT c.City FROM City c INNER JOIN Address a ON a.FK_City = c.ID INNER JOIN County co ON co.ID = a.FK_County WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1)"
# result = cursor.execute(sqlquery)
# cities = result.fetchall()
# print("Städte, mit Immobilien in mehr als einem Landkreis: ")
# for city in cities:
#     print(city[0])
#
# cursor.close()