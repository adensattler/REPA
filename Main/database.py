import sqlite3
import pandas as pd
import json

class DatabaseManager:
    
    _instance = None

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
   
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_name = db_name
            cls._instance.conn = None
        return cls._instance


    def create_database(self):
        with self.conn:
            # Create a SQLite connection and cursor
            c = self.conn.cursor()


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
            latitude REAL,
            longitude REAL,
            nearby_schools BLOB,
            nearby_cities BLOB,
            images TEXT,
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
        self.conn.commit()
        c.close()

    def fill_database(self, dataframe):
        with self.conn:
            c = self.conn.cursor()
            columns = list(dataframe.columns)
            columns = [column.replace('.', '_') for column in columns]
            for i, row in dataframe.iterrows():
                c.execute('INSERT INTO listings (zillow_ID, price, num_beds, num_baths, area, zipcode, living_area, house_type, zestimate, city, latitude, longitude, tax_ass_val) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                          (row['zpid'], row['hdpData.homeInfo.price'], row['hdpData.homeInfo.bedrooms'], row['hdpData.homeInfo.bathrooms'], row['area'], row['hdpData.homeInfo.zipcode'], row['hdpData.homeInfo.livingArea'], row['hdpData.homeInfo.homeType'], row['hdpData.homeInfo.zestimate'], row['hdpData.homeInfo.city'], row['hdpData.homeInfo.latitude'], row['hdpData.homeInfo.longitude'], row['hdpData.homeInfo.taxAssessedValue']))
        self.conn.commit()
        c.close()

    # This function given a zpid returns the raw json of a property
    # From the Database
    def get_JSON(self, zpid):
        with self.conn:
            zpid = str(zpid)
            c = self.conn.cursor()
            sql = 'SELECT raw_json FROM propertyDetails WHERE zillow_ID =' + zpid
            rows = c.execute(sql).fetchall()
            dataRaw = rows[0][0]
        c.close()
        return dataRaw



    def insert_property_db(self,zpid,data):
        with self.conn:
            c = self.conn.cursor()
            sql = 'SELECT COUNT(zillow_ID) FROM propertyDetails WHERE zillow_ID = ?'
            inDB = c.execute(sql, (zpid,)).fetchone()[0]
            if (inDB < 1):
                # Insert data into the table
                c.execute('INSERT INTO propertyDetails (zillow_ID,raw_json) VALUES (?,?)',(zpid , data))
                data = json.loads(self.get_JSON(zpid))
                
                #Insert data for each column
                self.update_property_db(zpid, "streetAddress" , data["data"]["address"]["streetAddress"])
                self.update_property_db(zpid, "price", data["data"]["price"])
                self.update_property_db(zpid, "num_beds", data["data"]["bedrooms"])
                self.update_property_db(zpid, "num_baths", data["data"]["bathrooms"])
                self.update_property_db(zpid, "zestimate", data["data"]["zestimate"])
                self.update_property_db(zpid, "sqft", data["data"]["adTargets"]["sqft"])
                self.update_property_db(zpid, "price_per_sqft", data["data"]["resoFacts"]["pricePerSquareFoot"])
                self.update_property_db(zpid, "property_tax", data["data"]["propertyTaxRate"])
    
                self.update_property_db(zpid, "latitude", data["data"]["adTargets"]["mlat"])
                self.update_property_db(zpid, "longitude", data["data"]["adTargets"]["mlong"])
                self.update_property_db(zpid, "house_type", data["data"]["homeType"])
    
                # TODO: Schools
                # TODO: Nearby Cities
    
                # TODO: Get more Images
                self.update_property_db(zpid, "images", data['data']['responsivePhotos'][0]['mixedSources']['jpeg'][7]['url'])
                self.update_property_db(zpid, "description", data["data"]["description"])
                self.conn.commit()
            c.close()
    
    



    def update_property_db(self, zpid, field, data):
        with self.conn:
            c = self.conn.cursor()
            sql = 'UPDATE propertyDetails SET ' + field + ' = "' + str(data) + '" WHERE zillow_ID = ' + zpid
            c.execute(sql)
        self.conn.commit()
        c.close()

    def get_value_from_property_db(self, zpid, key):
        with self.conn:
            c = self.conn.cursor()
            sql = "SELECT " + str(key) + " FROM propertyDetails WHERE zillow_ID = " + str(zpid)
            data = c.execute(sql).fetchone()
            self.conn.commit()
        c.close()
        return data[0][0]

# SOME HELPER FUNCTIONS
    def get_property_from_db(self, zpid):
        #Returns property data from an SQL query as a dictionary.
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            property = c.execute('SELECT zillow_ID, streetAddress, price, num_beds, num_baths, zestimate, sqft, price_per_sqft, house_type, property_tax, nearby_schools, nearby_cities, images, description, images FROM propertyDetails WHERE zillow_ID = ?', (zpid,)).fetchone()
        self.conn.commit()
        c.close()
        if property is not None:
            return dict(property)
        else:
            return None

    def get_prop_search_history(self):
        properties = self.sql_data_to_list_of_dicts("SELECT * FROM propertyDetails LIMIT 5")
        return properties

    def sql_data_to_list_of_dicts(self, select_query):
        # Returns data from an SQL query as a list of dicts.
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            things = c.execute(select_query).fetchall()
            unpacked = [{k: item[k] for k in item.keys()} for item in things]
        self.conn.commit()
        c.close()
        return unpacked

