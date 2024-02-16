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
        price INTEGER,
        num_beds INTEGER,
        num_baths INTEGER,
        zestimate INTEGER,
        sqft INTEGER,
        price_per_sqft INTEGER,
        house_type TEXT,
        property_tax REAL,
        nearby_schools BLOB,
        nearby_cities BLOB,
        images BLOB,
        description TEXT,
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
            
            #Insert data for each column
            update_property_db(zpid, "streetAddress" , data["data"]["address"]["streetAddress"])
            update_property_db(zpid, "price", data["data"]["price"])
            update_property_db(zpid, "num_beds", data["data"]["bedrooms"])
            update_property_db(zpid, "num_baths", data["data"]["bathrooms"])
            update_property_db(zpid, "zestimate", data["data"]["zestimate"])
            update_property_db(zpid, "sqft", data["data"]["adTargets"]["sqft"])
            update_property_db(zpid, "price_per_sqft", data["data"]["resoFacts"]["pricePerSquareFoot"])
            update_property_db(zpid, "property_tax", data["data"]["propertyTaxRate"])
            update_property_db(zpid, "house_type", data["data"]["homeType"])


            # TODO: Schools
            # TODO: Nearby Cities
            # TODO: images

            update_property_db(zpid, "description", data["data"]["description"])

    except Exception as e:
        print(f"Failed to execute. Query: insert_property_db\n with error:\n{e}")
    finally:
        conn.close()



def update_property_db(zpid, field, data):
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()
    sql = 'UPDATE propertyDetails SET ' + field + ' = "' + str(data) + '" WHERE zillow_ID = ' + zpid
    c.execute(sql)

    conn.commit()
    conn.close()

def get_value_from_property_db(zpid, key):
    conn = sqlite3.connect('zillow_listings.db')
    c = conn.cursor()
    sql = "SELECT " + str(key) + " FROM propertyDetails WHERE zillow_ID = " + str(zpid)
    data = c.execute(sql).fetchone()
    return data[0][0]

# SOME HELPER FUNCTIONS
def get_property_from_db(zpid):
    """Returns property data from an SQL query as a dictionary."""
    try:
        conn = sqlite3.connect('zillow_listings.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        property = cursor.execute('SELECT zillow_ID, streetAddress, price, num_beds, num_baths, zestimate, sqft, price_per_sqft, house_type, property_tax, nearby_schools, nearby_cities, images, description FROM propertyDetails WHERE zillow_ID = ?', (zpid,)).fetchone()
        if property is not None:
            return dict(property)
        else:
            return None
    except Exception as e:
        print(f"Failed to execute. Query: 'SELECT * FROM propertyDetails WHERE zillow_ID = ?'\n with error:\n{e}")
        return None
    finally:
        conn.close()

def get_prop_search_history():
    properties = sql_data_to_list_of_dicts("zillow_listings.db", "SELECT * FROM propertyDetails")
    return properties

def sql_data_to_list_of_dicts(path_to_db, select_query):
    """Returns data from an SQL query as a list of dicts."""
    try:
        conn = sqlite3.connect(path_to_db)
        conn.row_factory = sqlite3.Row
        things = conn.execute(select_query).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        conn.close()

