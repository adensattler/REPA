import sqlite3
import pandas as pd

def create_database(dataframe):
    # Create a SQLite connection and cursor
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()

    columns = list(dataframe.columns)
    columns = [column.replace('.', '_') for column in columns]

# Create the table with appropriate columns and constraints
    c.execute('''
    CREATE TABLE listings (
        zillow_ID INTEGER PRIMARY KEY NOT NULL,
        price INTEGER NOT NULL,
        no_of_beds INTEGER NOT NULL,
        no_of_baths INTEGER NOT NULL,
        area INTEGER NOT NULL,
        zipcode INTEGER NOT NULL,
        living_area INTEGER NOT NULL,
        house_type TEXT NOT NULL,
        zestimate INTEGER NOT NULL,
        city TEXT NOT NULL
    )
    ''')

    for i, row in dataframe.iterrows():
        c.execute('INSERT INTO listings (zillow_ID, price, no_of_beds, no_of_baths, area, zipcode, living_area, house_type, zestimate, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                  (row['zpid'], row['hdpData.homeInfo.price'], row['hdpData.homeInfo.bedrooms'], row['hdpData.homeInfo.bathrooms'], row['area'], row['hdpData.homeInfo.zipcode'], row['hdpData.homeInfo.livingArea'], row['hdpData.homeInfo.homeType'], row['hdpData.homeInfo.zestimate'], row['hdpData.homeInfo.city']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
