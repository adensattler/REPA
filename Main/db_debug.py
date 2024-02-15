import sqlite3 

conn = sqlite3.connect('zillow_listings.db')
c = conn.cursor()

c.execute(' DROP TABLE IF EXISTS propertyDetails;')
c.execute(' DROP TABLE IF EXISTS favoriteList')
c.execute(' DROP TABLE IF EXISTS listings;')

conn.commit()
conn.close()
