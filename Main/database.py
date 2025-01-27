import sqlite3
import json

class DatabaseManager:
    
    _instance = None

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
   
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
            zipcode INTEGER,
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
            thumbnail TEXT,
            description TEXT,
            monthly_rent REAL,
            cap_rate REAL,
            break_even REAL,
            thirty_year_mortgage REAL,
            fifteen_year_mortgage REAL,
            interest_est REAL,
            rel_price REAL,
            rel_price_comps REAL,
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
            c.execute('''
            CREATE TABLE IF NOT EXISTS nearby_listings (
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
        self.conn.commit()
        c.close()


    def fill_database(self, table, dataframe):
        with self.conn:
            c = self.conn.cursor()
            columns = list(dataframe.columns)
            columns = [column.replace('.', '_') for column in columns]
            for i, row in dataframe.iterrows():
                c.execute('INSERT INTO ' + table + ' (zillow_ID, price, num_beds, num_baths, area, zipcode, living_area, house_type, zestimate, city, latitude, longitude, tax_ass_val) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
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

                #For future: update data with the full JSON 
                # data = json.loads(self.get_JSON(zpid))
                data=json.loads(data)
                
                #Insert data for each column
                self.update_property_db(zpid, "streetAddress" , data["data"]["address"]["streetAddress"])
                self.update_property_db(zpid, "price", data["data"]["price"])
                self.update_property_db(zpid, "num_beds", data["data"]["bedrooms"])
                self.update_property_db(zpid, "num_baths", data["data"]["bathrooms"])
                self.update_property_db(zpid, "zestimate", data["data"]["zestimate"])
                self.update_property_db(zpid, "sqft", data["data"]["adTargets"]["sqft"])
                self.update_property_db(zpid, "price_per_sqft", data["data"]["resoFacts"]["pricePerSquareFoot"])
                self.update_property_db(zpid, "property_tax", data["data"]["propertyTaxRate"])
                self.update_property_db(zpid,"zipcode", data["data"]["zipcode"] )
    
                self.update_property_db(zpid, "latitude", data["data"]["adTargets"]["mlat"])
                self.update_property_db(zpid, "longitude", data["data"]["adTargets"]["mlong"])
                self.update_property_db(zpid, "house_type", data["data"]["homeType"])
                self.update_property_db(zpid, "fifteen_year_mortgage", data["data"]["mortgageRates"]["fifteenYearFixedRate"])
                self.update_property_db(zpid, "thirty_year_mortgage", data["data"]["mortgageRates"]["thirtyYearFixedRate"])
                self.update_property_db(zpid, "monthly_rent", data["data"]["rentZestimate"])

                # TODO: Schools
                # TODO: Nearby Cities
            
                # Loop through all images
                img_urls = []
                for img in data['data']['responsivePhotos']:
                    img_urls.append(img['mixedSources']['jpeg'][7]['url'])
                
                # Serialize the data (list of URLs) to JSON before storing in the database
                img_urls_json = json.dumps(img_urls)
                self.update_property_db(zpid, "images", img_urls_json)

                # Store 1st image as thumbnail for property_search page
                self.update_property_db(zpid, "thumbnail", data['data']['responsivePhotos'][0]['mixedSources']['jpeg'][7]['url'])

                self.update_property_db(zpid, "description", data["data"]["description"])
                self.conn.commit()    
            c.close()


    def update_property_db(self, zpid, field, data):
        with self.conn:
            c = self.conn.cursor()
            if field == 'images':
                # Use parameterized queries to handle special characters
                sql = 'UPDATE propertyDetails SET images = ? WHERE zillow_ID = ?'
                c.execute(sql, (data, zpid))
            else:
                sql = 'UPDATE propertyDetails SET ' + field + ' = "' + str(data) + '" WHERE zillow_ID = ' + zpid
                c.execute(sql)
        self.conn.commit()
        c.close()


    def get_value_from_property_db(self, zpid, key):
        with self.conn:
            c = self.conn.cursor()
            self.conn.row_factory = sqlite3.Row
            sql = "SELECT " + str(key) + " FROM propertyDetails WHERE zillow_ID = " + str(zpid)
            data = c.execute(sql).fetchone()
        self.conn.commit()
        c.close()
        return data[0]
    

    def get_images_from_property_db(self, zpid):
        with self.conn:
            c = self.conn.cursor()
            self.conn.row_factory = sqlite3.Row
            sql = "SELECT images FROM propertyDetails WHERE zillow_ID = ?"
            data = c.execute(sql, (zpid,)).fetchone()
        return data[0] if data else None


# SOME HELPER FUNCTIONS
    def get_property_from_db(self, zpid):
        #Returns property data from an SQL query as a dictionary.
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            # property = c.execute('SELECT zillow_ID, streetAddress, price, num_beds, num_baths, zestimate, sqft, price_per_sqft, house_type, property_tax, nearby_schools, nearby_cities, images, description, images, thirty_year_mortgage, fifteen_year_mortgage FROM propertyDetails WHERE zillow_ID = ?', (zpid,)).fetchone()
            property = c.execute('SELECT * FROM propertyDetails WHERE zillow_ID = ?', (zpid,)).fetchone()
        self.conn.commit()
        c.close()
        if property is not None:
            return dict(property)
        else:
            return None



    def get_prop_search_history(self, zpids):
        list = []
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            for z in zpids:
                list.extend(self.sql_data_to_list_of_dicts("SELECT * FROM propertyDetails WHERE zillow_ID = " + str(z)))
        self.conn.commit()
        c.close()
        return list

    def get_all_searches(self):
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            searches = c.execute('''SELECT * FROM propertyDetails''').fetchall()
        self.conn.commit()
        return [dict(ix) for ix in searches]

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


    def add_to_favorites(self, zpid):
        with self.conn:
            c = self.conn.cursor()
            # Check if the zpid already exists in the favoriteList to avoid duplicates
            c.execute("SELECT COUNT(*) FROM favoriteList WHERE zillow_ID = ?", (zpid,))
            if c.fetchone()[0] == 0:  # If not already in favorites
                c.execute("INSERT INTO favoriteList (zillow_ID) VALUES (?)", (zpid,))
        self.conn.commit()


    def get_favorite_properties(self):
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            favorites = c.execute('''SELECT pd.* FROM propertyDetails pd
                                  JOIN favoriteList fl ON pd.zillow_ID = fl.zillow_ID''').fetchall()
        self.conn.commit()
        return [dict(ix) for ix in favorites]


    def add_nearby_homes(self, zpid):
        with self.conn:
            lat = self.get_value_from_property_db(zpid, "latitude") 
            long = self.get_value_from_property_db(zpid, "longitude")
            # print("latitude is: "+ str(lat))
            # print("longitude is: "+ str(long))
            top = float(lat) + 0.2
            bottom = float(lat) - 0.2
            left = float(long) - 0.2
            right = float(long) + 0.2
            zillow_url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A"+str(left)+"%2C%22east%22%3A"+str(right)+"%2C%22south%22%3A"+str(bottom)+"%2C%22north%22%3A"+str(top)+"%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"
        self.conn.commit()
        return zillow_url
    

    def get_area_prices(self, zipcode):
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            prices = c.execute("SELECT price FROM nearby_listings WHERE zipcode = (?)",(zipcode,)).fetchall()
            return [dict(ix) for ix in prices]


    def remove_from_favorites(self, zipcode):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM favoriteList WHERE zillow_ID = ?", (zipcode,))
            conn.commit()


    def is_favorite(self, zpid):
        """Check if a property is marked as a favorite.

        Args:
            zpid (str): The Zillow Property ID to check.

        Returns:
            bool: True if the property is a favorite, False otherwise.
        """
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM favoriteList WHERE zillow_ID = ?", (zpid,))
            count = cursor.fetchone()[0]
            return count > 0
        
    def get_address(self, zpid):
        with self.conn as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT streetAddress FROM propertyDetails WHERE zillow_ID = ?", (zpid,)).fetchone()

    
