import sqlite3
import pandas as pd
import json

def create_database():
    # Create a SQLite connection and cursor
    conn = sqlite3.connect('zillow_listings.db')
    conn.row_factory = sqlite3.Row
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
        raw_json JSON,


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

# This function given a zpid returns the raw json of a property
# From the Database
def get_JSON(zpid):
    zpid = str(zpid)
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()

    sql = 'SELECT raw_json FROM propertyDetails WHERE zillow_ID =' +zpid
    rows = c.execute(sql).fetchall()
    dataRaw = rows[0][0]

    return dataRaw


# # INFO This function takes either a list of keys or a single key as well as the raw JSON
# # and gets the the specific key data from the database
# def data_from_JSON(keys, dataRaw):
#     if type(keys) is not list: keys = [keys]

#     response_values = []
#     data = json.loads(dataRaw)
#     for i in keys:
#        response_values.append(data.get(i))
#     return response_values

# # Heres an example of how these two functions would work together

# # jsonRaw = get_JSON(12947851)
# # data = data_from_JSON("is_success", jsonRaw)

# # the following also works:
# # data = data_from_JSON(["is_success", "address", "bedrooms", "bathrooms"], jsonRaw)



def insert_property_db(zpid,data):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('zillow_listings.db')
        c = conn.cursor()
        sql = 'SELECT COUNT(zillow_ID) FROM propertyDetails WHERE zillow_ID = ?'
        inDB = c.execute(sql, (zpid,)).fetchone()[0]
            
        if (inDB < 1):
            # Insert data into the table
            c.execute('INSERT INTO propertyDetails (zillow_ID,raw_json) VALUES (?,?)',(zpid , data))
            conn.commit()
            data = json.loads(get_JSON(zpid))
            update_property_db(zpid, "streetAddress" , data["data"]["address"]["streetAddress"])
    except Exception as e:
        print(f"Failed to execute. Query: insert_property_db\n with error:\n{e}")
    finally:
        conn.close()

def update_property_db(zpid, field, data):
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()
    sql = 'UPDATE propertyDetails SET ' + field + ' = "' + data + '" WHERE zillow_ID = ' + zpid
    c.execute(sql)

    conn.commit()
    conn.close()
