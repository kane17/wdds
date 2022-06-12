import csv
import sqlite3


def getCsv():
    csvfile = open('RealEstate_California-adapted-new.csv',
                   newline='')  # `with` statement available in 2.5+# csv.DictReader uses first line in file for column headings by default
    return csv.reader(csvfile, delimiter=',', quotechar='|')


database = sqlite3.connect('wdda_sem_db1.db')
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

    # insert country
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
        if lotAreUnit != 'lotAreaUnits':
            cursor.execute(insertQuery, (lotAreUnit,))

    # insert County
    insertQuery = "INSERT INTO County (County) VALUES (?)"
    for county in countyList:
        if county != 'county':
            cursor.execute(insertQuery, (county,))

    # insert State
    insertQuery = "INSERT INTO State (State, FK_Country) VALUES (?, ?)"
    for state in stateList:
        if state != 'state':
            cursor.execute(insertQuery, (state, 1))

    database.commit()


insertData()


def getCityId(cityTable, city):
    if len(cityTable) == 0:
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM City"""
        rows = cursor.execute(selectQuery)
        cityTable = rows.fetchall()
    for cityItem in cityTable:
        if city in cityItem:
            return cityTable, cityItem[0]
    raise Exception("City not found")


def getStateId(stateTable, state):
    if len(stateTable) == 0:
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM State"""
        rows = cursor.execute(selectQuery)
        stateTable = rows.fetchall()
    for stateItem in stateTable:
        if state in stateItem:
            return stateTable, stateItem[0]
    raise Exception("State not found")


def getCoordinatesId(coordinatesTable, longitude, latitude, hasBadGeoCode):
    if len(coordinatesTable) == 0:
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
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
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
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
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
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
            coordinatesTable, coordinatesId = getCoordinatesId(coordinatesTable, float(longitude), float(latitude),
                                                               int(hasBadGeoCode))
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
        # selectQuery = """SELECT ID FROM City WHERE City = ?"""
        selectQuery = """SELECT * FROM LotAreaUnit"""
        rows = cursor.execute(selectQuery)
        lotAreaUnitTable = rows.fetchall()
    for lotAreaUnitItem in lotAreaUnitTable:
        if lotAreaUnit in lotAreaUnitItem:
            return lotAreaUnitTable, lotAreaUnitItem[0]
    raise Exception("LotAreaUnit not found")


# insert LivingArea
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


def getCurrencyId():
    return 1


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


def getPropertyEntity(row):
    eventTable = tuple()
    homeTypeTable = tuple()
    propertyEntity = list()
    propertyEntity.append(row[21])
    propertyEntity.append(row[22])
    propertyEntity.append(row[23])
    propertyEntity.append(row[24])
    propertyEntity.append(row[26])
    propertyEntity.append(row[25])
    propertyEntity.append(row[27])
    propertyEntity.append(row[28])
    propertyEntity.append(row[29])
    propertyEntity.append(row[30])
    propertyEntity.append(row[31])
    propertyEntity.append(row[7])
    propertyEntity.append(row[10])
    propertyEntity.append(row[4])
    propertyEntity.append(row[3])
    propertyEntity.append(row[2])
    homeTypeTable, homeTypeId = getHomeTypeId(homeTypeTable, row[32])
    eventTable, eventId = getEventId(eventTable, row[5])
    propertyEntity.append(homeTypeId)
    propertyEntity.append(eventId)
    return propertyEntity


def insertPropertiesData():
    csv = getCsv()
    propertiesList = set()
    for row in csv:
        homeType = row[32]
        if homeType != 'homeType':
            propertyEntry = getPropertyEntity(row)
            propertiesList.add((
                propertyEntry[0], propertyEntry[1], propertyEntry[2], propertyEntry[3], propertyEntry[4],
                propertyEntry[5], propertyEntry[6], propertyEntry[7], propertyEntry[8], propertyEntry[9],
                propertyEntry[10], propertyEntry[11], propertyEntry[12], propertyEntry[13],
                propertyEntry[14], propertyEntry[15], propertyEntry[16], propertyEntry[17]))

    insertQuery = "INSERT INTO Properties (Bathrooms, Bedrooms, Buildingarea, Parking, HasGarage, Garagespaces, Levels, Pool, Spa, IsNewConstruction, HasPetsAllowed, PricePerSquareFoot, YearBuilt, IsForAuction, IsBankOwned, DatePosted, FK_HomeType, FK_Event) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insertQuery, propertiesList)

    database.commit()

    selectQuery = """SELECT * FROM Properties"""
    rows = cursor.execute(selectQuery)
    propertiesTable = rows.fetchall()
    return propertiesTable


propertiesTable = insertPropertiesData()


def getPropertiesId(propertiesTable, propertyFields):
    match = False
    for propertiesItem in propertiesTable:
        if (propertyFields[0] == str(propertiesItem[1]) and
                propertyFields[1] == str(propertiesItem[2]) and
                propertyFields[2] == str(propertiesItem[3]) and
                propertyFields[3] == str(propertiesItem[4]) and
                propertyFields[4] == str(propertiesItem[5]) and
                propertyFields[5] == str(propertiesItem[6]) and
                propertyFields[6] == propertiesItem[7] and
                propertyFields[7] == str(propertiesItem[8]) and
                propertyFields[8] == str(propertiesItem[9]) and
                propertyFields[9] == str(propertiesItem[10]) and
                propertyFields[10] == str(propertiesItem[11]) and
                propertyFields[11] == propertiesItem[12] and
                propertyFields[12] == propertiesItem[13] and
                propertyFields[13] == str(propertiesItem[14]) and
                propertyFields[14] == str(propertiesItem[15]) and
                propertyFields[15] == propertiesItem[16] and
                propertyFields[16] == propertiesItem[17] and
                propertyFields[17] == propertiesItem[18]):
            return propertiesItem[0]
    raise Exception("Properties not found")


def getPriceId(priceTable, price):
    if len(priceTable) == 0:
        selectQuery = """SELECT * FROM Price"""
        rows = cursor.execute(selectQuery)
        priceTable = rows.fetchall()
    for priceItem in priceTable:
        if price in priceItem:
            return priceTable, priceItem[0]
    raise Exception("Price not found")


def getAddressId(addressTable, address):
    if len(addressTable) == 0:
        selectQuery = """SELECT * FROM Address"""
        rows = cursor.execute(selectQuery)
        addressTable = rows.fetchall()
    for addressItem in addressTable:
        if address in addressItem:
            return addressTable, addressItem[0]
    raise Exception("Address not found")


def getLivingAreaId(livingAreaTable, lotAreaUnitTable, livingArea, lotAreaUnit):
    if len(livingAreaTable) == 0:
        selectQuery = """SELECT * FROM LivingArea"""
        rows = cursor.execute(selectQuery)
        livingAreaTable = rows.fetchall()
    lotAreaUnitTable, lotAreaUnitId = getLotAreaUnitId(lotAreaUnitTable, lotAreaUnit)
    for livingAreaItem in livingAreaTable:
        if int(livingArea) == livingAreaItem[1] and int(lotAreaUnitId) == livingAreaItem[3]:
            return livingAreaTable, lotAreaUnitTable, livingAreaItem[0]
    raise Exception("LivingArea not found")


def insertHouseData(propertiesTable):
    csv = getCsv()
    houseList = set()
    addressTable = tuple()
    priceTable = tuple()
    livingAreaTable = tuple()
    lotAreaUnitTable = tuple()
    counter = 0
    for row in csv:
        description = row[16]
        price = row[6]
        address = row[11]
        livingArea = row[18]
        lotAreaUnit = row[20]
        houseId = row[0]
        if description != 'description':
            counter += 1
            propertiesId = getPropertiesId(propertiesTable, getPropertyEntity(row))
            priceTable, priceId = getPriceId(priceTable, price)
            addressTable, addressId = getAddressId(addressTable, address)
            livingAreaTable, lotAreaUnitTable, livingAreaId = getLivingAreaId(livingAreaTable, lotAreaUnitTable,
                                                                              livingArea, lotAreaUnit)
            houseList.add((houseId, description, priceId, addressId, propertiesId, livingAreaId))
            print(counter)

    insertQuery = "INSERT INTO House (ID, Description, FK_Price, FK_Address, FK_Properties, FK_LivingArea) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(insertQuery, houseList)
    print('test')
    database.commit()


insertHouseData(propertiesTable)

cursor.close()

database.close()
