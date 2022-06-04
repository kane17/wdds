import sqlite3

# Datenbankverbindung herstellen
database = sqlite3.connect('C:/Users/larss/Downloads/wdda_sem_db1.db')
cursor = database.cursor()





# Aufgabe 2
def get_amount_of_buildings_built_after():

    yearBuilt = input(">>> type a year: ")
    sqlquery = "SELECT count(*) as 'Anzahl Häuser mit Baujahr "+ yearBuilt +"und höher' FROM House WHERE FK_Properties IN " \
               "(SELECT ID From Properties WHERE YearBuilt >= (?) AND YearBuilt != 'N/A');"
    result = cursor.execute(sqlquery, (yearBuilt,))
    amount = result.fetchone()
    print("Anzahl Häuser mit Baujahr", yearBuilt, "und höher (inkl. Jahr 9999): ", amount[0])
    print("!!!ATTENTION!!! There could be more houses with yearbuilt higher than "+yearBuilt+", but there are many entries with 'N/A' which have not been considered!")

#Aufgabe 3
# def get_amount_of_cities_with_more_than_one_house():
#     sqlquery = "SELECT DISTINCT c.City FROM City c LEFT JOIN Address a ON a.FK_City = c.ID LEFT JOIN County co ON co.ID = a.FK_County WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 3);"
#     cities = cursor.execute(sqlquery)
#     summarycities = cities.fetchall()
#     print("Städte, mit Immobilien in mehr als einem Landkreis:")
#     for x in summarycities:
#         print(x)

print("#-------------------")
print("# main programm: ")
print("#-------------------")

print("\ntask 2 from sql excercises...")
get_amount_of_buildings_built_after()

# print("\ntask 3 from sql excercises...")
# get_amount_of_cities_with_more_than_one_house()



cursor.close()
database.close()