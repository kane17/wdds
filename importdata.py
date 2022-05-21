import xlrd
import csv
import sqlite3

#book = xlrd.open_workbook("../../RealEstate_California-adapted.xlsx")
#sheet = book.sheet_by_name("Tabelle1")

csvfile = open('../../RealEstate_California-adapted-new.csv',newline='') # `with` statement available in 2.5+# csv.DictReader uses first line in file for column headings by default

priceList = set()
pricePerSquareFootList = set()
csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
for row in csvreader:
    #print(', '.join(row))
    priceList.add(row[6])
    pricePerSquareFootList.add(row[7])

print(priceList)
print(pricePerSquareFootList)





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