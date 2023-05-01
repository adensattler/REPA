import sqlite3
import csv

conn = sqlite3.connect('RealEstateProject.db')

cur = conn.cursor()

# Read the CSV file and get the header row
with open('/Users/jordan/Desktop/Software Engineering/dataframe.csv') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

# Create a new table with the header columns
query = f"CREATE TABLE RealEstate ({', '.join(header)})"
cur.execute(query)

# Insert data into the table
with open('path/to/data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = [row[column] for column in header]
        query = f"INSERT INTO RealEstate ({', '.join(header)}) VALUES ({', '.join(['?']*len(header))})"
        cur.execute(query, values)

# Commit changes and close the connection
conn.commit()
conn.close()

