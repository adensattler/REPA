import sqlite3
import pandas as pd

def create_database():
    # Create a SQLite connection and cursor
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()

    # c.execute('DROP TABLE IF EXISTS listings;')

# Create the table with appropriate columns and constraints
    c.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        zillow_ID INTEGER PRIMARY KEY NOT NULL,
        price INTEGER NOT NULL,
        num_beds INTEGER NOT NULL,
        num_baths INTEGER NOT NULL,
        area INTEGER NOT NULL,
        zipcode INTEGER NOT NULL,
        living_area INTEGER NOT NULL,
        house_type TEXT NOT NULL,
        zestimate INTEGER NOT NULL,
        city TEXT NOT NULL,
        latitude INTEGER NOT NULL,
        longitude INTEGER NOT NULL,
        tax_ass_val INTEGER NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS propertyDetails(
        zillow_ID INTEGER NOT NULL,
        streetAddress TEXT,

        CONSTRAINT zillow_ID_FK FOREIGN KEY (zillow_ID)
        REFERENCES listings(zillow_ID)
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS favoriteList(
        zillow_ID INTEGER NOT NULL,
        
        CONSTRAINT zillow_ID_FK FOREIGN KEY (zillow_ID)
        REFERENCES listings(zillow_ID)
    )

              ''')
    conn.commit()
    conn.close()

def fill_database(dataframe):
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()
    columns = list(dataframe.columns)
    columns = [column.replace('.', '_') for column in columns]
    for i, row in dataframe.iterrows():
        c.execute('INSERT INTO listings (zillow_ID, price, num_beds, num_baths, area, zipcode, living_area, house_type, zestimate, city, latitude, longitude, tax_ass_val) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                  (row['zpid'], row['hdpData.homeInfo.price'], row['hdpData.homeInfo.bedrooms'], row['hdpData.homeInfo.bathrooms'], row['area'], row['hdpData.homeInfo.zipcode'], row['hdpData.homeInfo.livingArea'], row['hdpData.homeInfo.homeType'], row['hdpData.homeInfo.zestimate'], row['hdpData.homeInfo.city'], row['hdpData.homeInfo.latitude'], row['hdpData.homeInfo.longitude'], row['hdpData.homeInfo.taxAssessedValue']))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_property_db(zpid):
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()

