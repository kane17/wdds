import csv
import sqlite3


def getCsv():
    csvfile = open('../../RealEstate_California-adapted-new.csv',newline='') # `with` statement available in 2.5+# csv.DictReader uses first line in file for column headings by default
    return csv.reader(csvfile, delimiter=',', quotechar='|')

database = sqlite3.connect('../wdda_sem_db1.db')
cursor = database.cursor()

# Diese Funktion lädt die Daten der normalisierten Tabellen in die Datenbank. Diese Funktion muss zuerst ausgeführt
# werden bevor die Daten der Address, House, etc. importiert werden können, da die Einträge schon existieren müssen
# für die FK.
def insertData():

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

insertData()

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

# insert Address
def insertAddressData():
    csv = getCsv()
    addressList = set()
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
            addressList.add((address, cityId, stateId, zipcodeId, coordinatesId, countyId))

    insertQuery = "INSERT INTO Address (Address, FK_City, FK_State, FK_Zipcode, FK_Coordinates, FK_County) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(insertQuery, addressList)

    database.commit()

insertAddressData()

def getLotAreaUnitId(lotAreaUnitTable, lotAreaUnit):
    if lotAreaUnit == '':
        return lotAreaUnitTable, 0
    if len(lotAreaUnitTable) == 0:
        #selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM LotAreaUnit"""
        rows = cursor.execute(selectQuery)
        lotAreaUnitTable = rows.fetchall()
    for lotAreaUnitItem in lotAreaUnitTable:
        if lotAreaUnit in lotAreaUnitItem:
            return lotAreaUnitTable, lotAreaUnitItem[0]
    raise Exception("LotAreaUnit not found")

#insert LivingArea
def insertLivingAreaData():
    csv = getCsv()
    livingAreaList = set()
    lotAreaUnitTable = tuple()
    for row in csv:
        livingArea = row[18]
        livingAreaValue = row[19]
        lotAreaUnit = row[20]
        if livingArea != 'livingArea':
            lotAreaUnitTable, lotAreaUnitId = getLotAreaUnitId(lotAreaUnitTable, lotAreaUnit)
            livingAreaList.add((livingArea, livingAreaValue, lotAreaUnitId))

    insertQuery = "INSERT INTO LivingArea (LivingArea, LivingAreaValue, FK_LotAreaUnit) VALUES (?, ?, ?)"
    cursor.executemany(insertQuery, livingAreaList)

    database.commit()

insertLivingAreaData()

# TODO: ausprogrammieren?
def getCurrencyId():
    return 1
# if currency == '':
    #     return currencyTable, 0
    # if len(currencyTable) == 0:
    #     #selectQuery = """SELECT ID FROM City WHERE City = ?"""
    #     selectQuery = """SELECT * FROM LotAreaUnit"""
    #     rows = cursor.execute(selectQuery)
    #     lotAreaUnitTable = rows.fetchall()
    # for currencyItem in currencyTable:
    #     if currency in currencyItem:
    #         return currencyTable, currencyItem[0]
    # raise Exception("LotAreaUnit not found")

def insertPrices():
    csv = getCsv()
    priceList = set()
    currencyTable = tuple()
    for row in csv:
        price = row[6]
        if price != 'price':
            currencyId = getCurrencyId()
            priceList.add((price, currencyId))

    insertQuery = "INSERT INTO Price (Price, FK_Currency) VALUES (?, ?)"
    cursor.executemany(insertQuery, priceList)
    database.commit()


insertPrices()


def getHomeTypeId(homeTypeTable, homeType):
    if homeType == '':
        return homeTypeTable, 0
    if len(homeTypeTable) == 0:
        selectQuery = """SELECT * FROM HomeType"""
        rows = cursor.execute(selectQuery)
        homeTypeTable = rows.fetchall()
    for homeTypeItem in homeTypeTable:
        if homeType in homeTypeItem:
            return homeTypeTable, homeTypeItem[0]
    raise Exception("HomeType not found")

def getEventId(eventTable, event):
    if event == '':
        return eventTable, 0
    if len(eventTable) == 0:
        selectQuery = """SELECT * FROM Event"""
        rows = cursor.execute(selectQuery)
        eventTable = rows.fetchall()
    for eventItem in eventTable:
        if event in eventItem:
            return eventTable, eventItem[0]
    raise Exception("Event not found")

def insertPropertiesData():
    csv = getCsv()
    propertiesList = set()
    eventTable = tuple()
    homeTypeTable = tuple()
    for row in csv:
        bathrooms = row[21]
        bedrooms = row[22]
        buildingArea = row[23]
        parking = row[24]
        garageSpaces = row[25]
        hasGarage = row[26]
        levels = row[27]
        pool = row[28]
        spa = row[29]
        isNewConstruction = row[30]
        hasPetsAllowed = row[31]
        homeType = row[32]
        pricePerSquareFoot = row[7]
        yearBuilt = row[10]
        isForAuction = row[4]
        isBankOwned = row[3]
        event = row[5]
        datePosted = row[2]
        if bathrooms != 'bathrooms':
            homeTypeTable, homeTypeId = getHomeTypeId(homeTypeTable, homeType)
            eventTable, eventId = getEventId(eventTable, event)
            propertiesList.add((bathrooms, bedrooms, buildingArea, parking, hasGarage, garageSpaces, levels, pool, spa, isNewConstruction, hasPetsAllowed, pricePerSquareFoot, yearBuilt, isForAuction, isBankOwned, datePosted, homeTypeId, eventId))

    insertQuery = "INSERT INTO Properties (Bathrooms, Bedrooms, Buildingarea, Parking, HasGarage, Garagespaces, Levels, Pool, Spa, IsNewConstruction, HasPetsAllowed, PricePerSquareFoot, YearBuilt, IsForAuction, IsBankOwned, DatePosted, FK_HomeType, FK_Event) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insertQuery, propertiesList)

    database.commit()


insertPropertiesData()

# selectQuery = """SELECT * FROM Properties"""
# a = cursor.execute(selectQuery)
#
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)
#
# print(len(rows))

cursor.close()

database.close()

