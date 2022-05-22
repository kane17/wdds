import csv
import sqlite3


def getCsv():
    csvfile = open('../../RealEstate_California-adapted-new.csv',newline='') # `with` statement available in 2.5+# csv.DictReader uses first line in file for column headings by default
    return csv.reader(csvfile, delimiter=',', quotechar='|')


# Country
countryList = set()
zipcodeList = set()
cityList = set()
currencyList = set()
eventList = set()
homeTypeList = set()
lotAreaUnitList = set()
countyList = set()
stateList = set()

csvreader = getCsv()
for row in csvreader:
    countryList.add(row[1])
    zipcodeList.add(row[12])
    cityList.add(row[8])
    currencyList.add(row[17])
    eventList.add(row[5])
    homeTypeList.add(row[32])
    lotAreaUnitList.add(row[20])
    countyList.add(row[33])
    stateList.add(row[9])

database = sqlite3.connect('../wdda_sem_db1.db')
cursor = database.cursor()

#insert country
insertQuery = "INSERT INTO Country (Country) VALUES (?)"
for country in countryList:
    # Execute sql Query
    if country != 'country':
        cursor.execute(insertQuery, (country,))


newreader = getCsv()
# insert coordinates
insertQuery = "INSERT INTO Coordinates (Longitude, Latitude, HasBadGeoCoordinates) VALUES (?, ?, ?)"
for row in newreader:
    longitude = row[13]
    latitude = row[14]
    hasBadGeoCode = row[15]
    if (longitude != 'longitude') & (latitude != 'latitude') & (hasBadGeoCode != 'hasBadGeocode'):
        cursor.execute(insertQuery, (longitude, latitude, hasBadGeoCode,))


# insert Zipcodes
insertQuery = "INSERT INTO Zipcode (Zipcode) VALUES (?)"
for zipcode in zipcodeList:
    if zipcode != 'zipcode':
        cursor.execute(insertQuery, (zipcode,))


# insert Cities
insertQuery = "INSERT INTO City (City) VALUES (?)"
for city in cityList:
    if city != 'city':
        cursor.execute(insertQuery, (city,))


# insert Currencies
insertQuery = "INSERT INTO Currency (Currency) VALUES (?)"
for currency in currencyList:
    if currency != 'currency':
        cursor.execute(insertQuery, (currency,))


# insert Events
insertQuery = "INSERT INTO Event (Event) VALUES (?)"
for event in eventList:
    if event != 'event':
        cursor.execute(insertQuery, (event,))

# insert HomeType
insertQuery = "INSERT INTO HomeType (HomeType) VALUES (?)"
for homeType in homeTypeList:
    if homeType != 'homeType':
        cursor.execute(insertQuery, (homeType,))


# insert LotAreaUnit
insertQuery = "INSERT INTO LotAreaUnit (LotAreaUnit) VALUES (?)"
for lotAreUnit in lotAreaUnitList:
    if lotAreUnit != 'lotAreUnits':
        cursor.execute(insertQuery, (lotAreUnit,))

# insert County
insertQuery = "INSERT INTO County (County) VALUES (?)"
for county in countyList:
    if county != 'county':
        cursor.execute(insertQuery, (county,))

# insert State
#TODO: Insert from select
insertQuery = "INSERT INTO State (State, FK_Country) VALUES (?, ?)"
for state in stateList:
    if state != 'state':
        cursor.execute(insertQuery, (state, 1))



database.commit()


def getCityId(city):
    selectQuery = """SELECT ID FROM City WHERE City = ?"""
    a = cursor.execute(selectQuery, (city,))
    return a.fetchone()

def getStateId(state):
    selectQuery = """SELECT ID FROM State WHERE State = ?"""
    a = cursor.execute(selectQuery, (state,))
    return a.fetchone()

def getCoordinatesId(longitude, latitude, hasBadGeoCode):
    selectQuery = """SELECT ID FROM Coordinates WHERE Longitude = ? AND Latitude = ? AND HasBadGeoCoordinates = ?"""
    a = cursor.execute(selectQuery, (longitude, latitude, hasBadGeoCode,))
    return a.fetchone()

def getCountyId(county):
    selectQuery = """SELECT ID FROM County WHERE County = ?"""
    a = cursor.execute(selectQuery, (county,))
    return a.fetchone()

def getzipcodeid(zipcode):
    selectQuery = """SELECT ID FROM Zipcode WHERE Zipcode = ?"""
    a = cursor.execute(selectQuery, (zipcode,))
    return a.fetchone()

# insert State
csv = getCsv()
insertQuery = "INSERT INTO Address (Address, FK_City, FK_State, FK_Zipcode, FK_Coordinates, FK_County) VALUES (?, ?, ?, ?, ?, ?)"
addressList = []
for row in csv:
    address = row[11]
    city = row[8]
    state = row[9]
    longitude = row[13]
    latitude = row[14]
    hasBadGeoCode = row[15]
    county = row[33]
    zipcode = row[12]
    if address != 'streetAddress':
        cityId = getCityId(city)
        stateId = getStateId(state)
        coordinatesId = getCoordinatesId(longitude, latitude, hasBadGeoCode)
        countyId = getCountyId(county)
        zipcodeId = getzipcodeid(zipcode)
        addressList.append((address, cityId, stateId, zipcodeId, coordinatesId, countyId))

cursor.executemany(insertQuery, addressList)

database.commit()

selectQuery = """SELECT * FROM Address"""
a = cursor.execute(selectQuery)

rows = cursor.fetchall()

for row in rows:
    print(row)

print(len(rows))

cursor.close()

database.close()






# print(countryList)
# #print(coordinatesLatitudeList)
# print(coordinatesLongitudeList)
# print(hasBadGeoCodesList)
# print(zipcodeList)
# print(cityList)
# print(currencyList)
# print(eventList)
# print(homeTypeList)
# print(lotAreaUnitList)





# 0. Normalisierte Tabellen manuell in SQL abfüllen mit INSERT
# 1. wir iterieren das ganze csv für sömtliche Daten
# 2. sämtliche daten abfüllen
# 3. Foreign Keys korrekt setzen innerhalb Schlaufe
# 4. done




# to_db = [(i['col1'], i['col2']) for i in dr]
#
#
# database = sqlite3.connect('../wdda_sem_db1.db')
#
# # Get the cursor, which is used to traverse the database, line by line
# cursor = database.cursor()
#
# #City
# queryCity = """INSERT INTO City (City) """
#
#
# # Create the INSERT INTO sql query
# query = """INSERT INTO orders (product, customer_type, rep, date, actual, expected, open_opportunities, closed_opportunities, city, state, zip, population, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#
# # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
# for r in range(1, sheet.nrows):
#     product		= sheet.cell(r,).value
#     customer	= sheet.cell(r,1).value
#     rep			= sheet.cell(r,2).value
#     date		= sheet.cell(r,3).value
#     actual		= sheet.cell(r,4).value
#     expected	= sheet.cell(r,5).value
#     open		= sheet.cell(r,6).value
#     closed		= sheet.cell(r,7).value
#     city		= sheet.cell(r,8).value
#     state		= sheet.cell(r,9).value
#     zip			= sheet.cell(r,10).value
#     pop			= sheet.cell(r,11).value
#     region	= sheet.cell(r,12).value
#
#     # Assign values from each row
#     values = (product, customer, rep, date, actual, expected, open, closed, city, state, zip, pop, region)
#
#     # Execute sql Query
#     cursor.execute(query, values)
#
# # Close the cursor
# cursor.close()
#
# # Commit the transaction
# database.commit()
#
# # Close the database connection
# database.close()