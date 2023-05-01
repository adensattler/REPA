import sqlite3

conn = sqlite3.connect('RealEstateProject.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE AreaInformation(
                User_ID INTEGER PRIMARY KEY NOT NULL,
                Product_ID INTEGER NOT NULL,
                Name TEXT NOT NULL,
                Gender TEXT NOT NULL,
                AGE INTEGER NOT NULL,
                CITY TEXT);
                ''')
conn.commit()
