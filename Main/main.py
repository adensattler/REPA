import pandas as pd
from data_acquisition import get_listings
from create_database import create_database
from analysis import perform_analysis

api_key = "1d06fd5a-f8a8-4204-bf67-628653b0aa23"
listing_url = "https://www.zillow.com/denver-county-co/houses/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Tampa%2C%20FL%22%2C%22mapBounds%22%3A%7B%22north%22%3A39.914247%2C%22east%22%3A-104.600296%2C%22south%22%3A39.614431%2C%22west%22%3A-105.109927%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A1000000%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22built%22%3A%7B%22min%22%3A1940%7D%2C%22doz%22%3A%7B%22value%22%3A%2290%22%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A4948%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22sche%22%3A%7B%22value%22%3Afalse%7D%2C%22schm%22%3A%7B%22value%22%3Afalse%7D%2C%22schh%22%3A%7B%22value%22%3Afalse%7D%2C%22schp%22%3A%7B%22value%22%3Afalse%7D%2C%22schr%22%3A%7B%22value%22%3Afalse%7D%2C%22schc%22%3A%7B%22value%22%3Afalse%7D%2C%22schu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A989%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D"

listing_response = get_listings(api_key, listing_url)

# stores the columns we are interested in
cols = ['zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.zipcode', 'beds', 'baths', 'area', 'hdpData.homeInfo.zestimate']

# Takes all of the data and converts it into normalized, tabular data (.json_normalize)
den_listings = pd.json_normalize(listing_response["data"]["cat1"]["searchResults"]["mapResults"])
selected_den_listings = den_listings.loc[:, cols].dropna(thresh=7)

create_database(selected_den_listings)
perform_analysis()
