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

def insertData():
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
            cursor.execute(insertQuery, (float(longitude), float(latitude), hasBadGeoCode,))


    # insert Zipcodes
    insertQuery = "INSERT INTO Zipcode (Zipcode) VALUES (?)"
    for zipcode in zipcodeList:
        if (zipcode != 'zipcode') and (zipcode != ''):
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

# insertData()

def getCityId(cityTable, city):
    if len(cityTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM City"""
        rows = cursor.execute(selectQuery)
        cityTable = rows.fetchall()
    for cityItem in cityTable:
        if city in cityItem:
            return cityTable, cityItem[0]
    raise Exception("City not found")

def getStateId(stateTable, state):
    if len(stateTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM State"""
        rows = cursor.execute(selectQuery)
        stateTable = rows.fetchall()
    for stateItem in stateTable:
        if state in stateItem:
            return stateTable, stateItem[0]
    raise Exception("State not found")

def getCoordinatesId(coordinatesTable, longitude, latitude, hasBadGeoCode):
    if len(coordinatesTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM Coordinates"""
        rows = cursor.execute(selectQuery)
        coordinatesTable = rows.fetchall()
    for coordinatesItem in coordinatesTable:
        # valLong = '%.7f'%(longitude)
        if longitude in coordinatesItem:
            if latitude in coordinatesItem:
                if hasBadGeoCode in coordinatesItem:
                    coordinatesTable.remove(coordinatesItem)
                    return coordinatesTable, coordinatesItem[0]
    raise Exception("Coordinates not found")

def getCountyId(countyTable, county):
    if len(countyTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM County"""
        rows = cursor.execute(selectQuery)
        countyTable = rows.fetchall()
    for countyItem in countyTable:
        if county in countyItem:
            return countyTable, countyItem[0]
    raise Exception("County not found")


def getZipcodeId(zipcodeTable, zipcode):
    if zipcode == '':
        return zipcodeTable, 0
    if len(zipcodeTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM Zipcode"""
        rows = cursor.execute(selectQuery)
        zipcodeTable = rows.fetchall()
    for zipcodeItem in zipcodeTable:
        if int(zipcode) in zipcodeItem:
            return zipcodeTable, zipcodeItem[0]
    raise Exception("Zipcode not found")

# insert State
csv = getCsv()
addressList = []
cityTable = tuple()
stateTable = tuple()
coordinatesTable = tuple()
countyTable = tuple()
zipcodeTable = tuple()
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
        cityTable, cityId = getCityId(cityTable, city)
        stateTable, stateId = getStateId(stateTable, state)
        coordinatesTable, coordinatesId = getCoordinatesId(coordinatesTable, float(longitude), float(latitude), int(hasBadGeoCode))
        countyTable, countyId = getCountyId(countyTable, county)
        zipcodeTable, zipcodeId = getZipcodeId(zipcodeTable, zipcode)
        addressList.append((address, cityId, stateId, zipcodeId, coordinatesId, countyId))

insertQuery = "INSERT INTO Address (Address, FK_City, FK_State, FK_Zipcode, FK_Coordinates, FK_County) VALUES (?, ?, ?, ?, ?, ?)"
cursor.executemany(insertQuery, addressList)

print(addressList)
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