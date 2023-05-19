import sqlite3
import pandas as pd

def create_database(dataframe):
    # Create a SQLite connection and cursor
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()

    # Create the "listings" table with the desired schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            zillow_ID INTEGER PRIMARY KEY NOT NULL,
            price INTEGER NOT NULL,
            zipcode INTEGER NOT NULL,
            no_of_beds INTEGER NOT NULL,
            no_of_baths INTEGER NOT NULL,
            area INTEGER NOT NULL,
            zestimate INTEGER NOT NULL
        )
    ''')

    for i, row in dataframe.iterrows():
        c.execute('INSERT INTO listings (zillow_ID, price, zipcode, no_of_beds, no_of_baths, area, zestimate) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                  (row['zpid'], row['hdpData.homeInfo.price'], row['hdpData.homeInfo.zipcode'], row['beds'], row['baths'], row['area'], row['hdpData.homeInfo.zestimate']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
