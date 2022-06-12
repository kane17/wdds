import sqlite3

# Datenbankverbindung herstellen
database = sqlite3.connect('wdda_sem_db1.db')
cursor = database.cursor()


# Aufgabe 2
def get_amount_of_buildings_built_after():
    year_built = input(">>> type a year: ")
    # Das Query selektiert alle Häuser, welche älter sind als das Baujahr, welches vom Benutzer eingegeben wurde.
    query = """SELECT count(*) as 'Anzahl Häuser mit Baujahr " + year_built + "und höher' FROM House 
                WHERE FK_Properties IN (SELECT ID From Properties WHERE YearBuilt > (?) AND YearBuilt != 'N/A' 
                AND YearBuilt != '9999');"""
    # Hier wird das Query ausgeführt.
    result = cursor.execute(query, (year_built,))
    # Hier wird die gesuchte Zahl aus dem Resultat geladen.
    amount = result.fetchone()
    print("Anzahl Häuser mit Baujahr nach ", year_built, ": ", amount[0])
    print(
        "!!!ATTENTION!!! There could be more houses with yearbuilt higher than "
        + year_built + ", but there are many entries with 'N/A' which have not been considered!")


# Aufgabe 3: Da es nicht Teil der Aufgabe war, kurzer Kommentar
def get_amount_of_cities_with_more_than_one_house():
    # Selektiert alle Städte aus der Datenbank mit Häusern in mehreren Counties
    query = """SELECT DISTINCT c.City FROM City c 
            LEFT JOIN Address a ON a.FK_City = c.ID
            LEFT JOIN County co ON co.ID = a.FK_County 
            WHERE ((SELECT COUNT(DISTINCT Address.FK_County) FROM Address WHERE Address.FK_City=c.ID) > 1);"""
    result = cursor.execute(query)
    cities = result.fetchall()
    print("Städte, mit Immobilien in mehr als einem Landkreis:")
    print(cities)


# Aufgabe 4: Da es nicht Teil der Aufgabe war, kurzer Kommentar
def select_cities_by_avg_price():
    # Selektiert die Städte absteigend sortiert nach dem Durchschnittlichem Immobilienpreis.
    query = """SELECT c.City, ROUND(AVG(p.Price), 2) AS 'Durchschnittlicher Preis' FROM House h
    LEFT JOIN Address a ON a.ID = h.FK_Address
    LEFT JOIN Price p ON h.FK_Price = p.ID
    LEFT JOIN City c ON c.ID = a.FK_City GROUP BY c.City ORDER BY ROUND(AVG(p.Price), 2) DESC;"""

    result = cursor.execute(query)

    for entry in result.fetchall():
        print(entry)


# Aufgabe 5: Da es nicht Teil der Aufgabe war, kurzer Kommentar
def select_cities_with_sqftprices_over_average():
    # Selektiert alle Städte und deren Preis Pro Quadratfuss, welcher über dem Durchschnitt liegt.
    query = """SELECT c.City, ROUND(AVG(prop.PricePerSquareFoot), 2) AS PricePerSquareFoot FROM House h
        LEFT JOIN Address a ON a.ID = h.FK_Address
        LEFT JOIN City c ON c.ID = a.FK_City
        LEFT JOIN Properties prop ON prop.ID = h.FK_Properties
    WHERE CAST(PricePerSquareFoot AS FLOAT) > CAST((SELECT ROUND(AVG(prop.PricePerSquareFoot), 2)
    AS 'Preis Pro Quadratmeter'
    FROM House h LEFT JOIN Properties prop ON prop.ID = h.FK_Properties 
    WHERE prop.PricePerSquareFoot != 'N/A') AS FLOAT) GROUP BY c.City;"""

    result = cursor.execute(query)

    print("{:<28} {:<35}".format('City', 'Price per SquareFoot'))
    for entry in result.fetchall():
        city, price_per_square_foot = entry
        print("{:<28} {:<35}".format(city, price_per_square_foot))


# Aufgabe 6
def select_offers_for_city():
    # Der User kann hier eine Stadt eingeben
    city = str(input(">>> type a city: "))
    # Das Query selektiert den HomeType, Price und Description aller Häuser einer Stadt, welche ein Angebot haben,
    # also einen Event mit Typ "Listed for sale" haben.
    query = """SELECT HT.HomeType, P2.Price, h.Description  FROM City c
        LEFT JOIN Address a ON a.FK_City = c.ID
        LEFT JOIN House h ON h.FK_Address = a.ID
        LEFT JOIN Properties P on h.FK_Properties = P.ID
        LEFT JOIN HomeType HT on P.FK_HomeType = HT.ID
        LEFT JOIN Event E on P.FK_Event = E.ID
        LEFT JOIN Price P2 on h.FK_Price = P2.ID
    WHERE c.City = ? AND E.Event = 'Listed for sale';"""

    # Hier wird das parametrisierte Query ausgeführt. Speziell ist das Tupel, womit der Parameter City mitgegeben
    # werden muss.
    result = cursor.execute(query, (city,))

    # In einer Loop werden die gesuchten Einträge ausgegeben.
    for entry in result.fetchall():
        print(entry)


print("#-------------------")
print("# main programm: ")
print("#-------------------")

print("\ntask 2 from sql excercises...")
get_amount_of_buildings_built_after()

print("\ntask 3 from sql excercises...")
get_amount_of_cities_with_more_than_one_house()

print("\ntask 4 from sql excercises...")
select_cities_by_avg_price()

print("\ntask 5 from sql excercises...")
select_cities_with_sqftprices_over_average()

print("\ntask 6 from sql excercises...")
select_offers_for_city()

print("\nTeil B der Aufgabenstellung wäre somit beendet.")

# Datenbankverbindung schliessen nach Ausführung aller Statements.
cursor.close()
database.close()
