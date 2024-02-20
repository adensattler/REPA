import re
import json
import requests
import pandas as pd
from database import DatabaseManager

database = DatabaseManager('zillow_listings.db')

def get_listings_gui(url:str, api_key:str)->str:
    scraper_api_url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    api_query_string = {
    "api_key": api_key,
    "url": url
    }

    api_response = requests.get(scraper_api_url, params=api_query_string)    
    # Successful API call: Status 200
    if api_response.status_code != 200:
        return ""

    data = api_response.json()

    num_of_properties_fetched = data["data"]["categoryTotals"]["cat1"]["totalResultCount"]

    # Store the columns we are interested in
    columns_of_interest = [
        'zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.bedrooms', 'hdpData.homeInfo.bathrooms', 'area',
        'hdpData.homeInfo.zipcode', 'hdpData.homeInfo.livingArea', 'hdpData.homeInfo.homeType', 'hdpData.homeInfo.zestimate', 'hdpData.homeInfo.city', 'hdpData.homeInfo.latitude', 'hdpData.homeInfo.longitude',
        'hdpData.homeInfo.taxAssessedValue'
    ]

    # Get DataFrame from .json
    den_listings = pd.json_normalize(data["data"]["cat1"]["searchResults"]["mapResults"])
    
    selected_den_listings = den_listings.loc[:, columns_of_interest].dropna(thresh=13) # Discard rows with over 13 null values
    database.fill_database(selected_den_listings)

    return f"{num_of_properties_fetched} properties fetched."


def get_listings(api_key, listing_url):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    response = requests.get(url, params=querystring)
    data = response.json()

    # Print the keys for the "data"
    print(data['data'].keys())

    # Print the number of homes fetched by the search
    numProperties = data["data"]["categoryTotals"]["cat1"]["totalResultCount"]
    print("Count of properties:", numProperties)

    return data


# get property detail
def get_property_detail(api_key, zpid):
  url = "https://app.scrapeak.com/v1/scrapers/zillow/property"

  querystring = {
      "api_key": api_key,
      "zpid": zpid
  }

  return requests.request("GET", url, params=querystring)

# Temporary function to examine API reponse
def save_api_response(api_key, zpid):
    response = get_property_detail(api_key, zpid)

    if response.status_code == 200: # Successful API call: Status 200
        data = response.json()

        with open("property_detail.json", "w") as json_file:
            json.dump(data, json_file)
        
        print("Data saved to property_detail.json successfully.")
    else:
        print(f"Error: {response.status_code} - {response.reason}")

def get_image_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        url = data['data']['responsivePhotos'][0]['mixedSources']['jpeg'][7]['url']
        response = requests.get(url)
    if response.status_code == 200:
        with open("property_image.jpg", 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image. Status code:", response.status_code)




def organize_property_details(api_key, zpid):
    response = get_property_detail(api_key, zpid)
    data = pd.json_normalize(response.json()['data'])
    prop_detail_dict = {}

    cities = []
    for _ in range(len(data['nearbyCities'][0])):
        cities.append(data['nearbyCities'][0][_]['name'])

    comps = []
    for _ in range(len(data['comps'][0])):
        comps.append(f"https://zillow.com/{data['comps'][0][_]['hdpUrl']}")
        
    schools = []
    for _ in range(len(data['schools'][0])):
        schools.append(f"school name: {data['schools'][0][_]['name']}\ndistance: {data['schools'][0][_]['distance']} miles\n"
              f"school rating: {data['schools'][0][_]['rating']}\nschool level: {data['schools'][0][_]['level']}")

    # price_hist = []
    # for i in range(len(data['priceHistory'][0])):
    #     price_hist.append(f"date: {data['priceHistory'][0][i]['date']}\nprice: {data['priceHistory'][0][i]['price']}\n"
    #         f"price per sqft: {data['priceHistory'][0][i]['pricePerSquareFoot']}")

    df_price_hist = pd.DataFrame(data['priceHistory'].iloc[0], index=None)
    cols = ['date', 'price', 'pricePerSquareFoot', 'priceChangeRate', 'event']
    df_price_hist = df_price_hist[cols]

    if len(data.columns) == 0:
        return prop_detail_dict, df_price_hist
    else:
        prop_detail_dict = {
            'street address': [data['streetAddress'][0] + ' ' + data['zipcode'][0]],
            'year built': [data['adTargets.yrblt'][0]],
            'nearby cities': cities,
            'comps': comps,
            'schools': schools,
            'description': [data['description'][0]]
        }

        return prop_detail_dict, df_price_hist

def get_description(api_key, zpid):
    api_response = get_property_detail(api_key, zpid)    

    if api_response.status_code != 200: # Successful API call: Status 200
        return ""
    else:
        data = pd.json_normalize(api_response.json()['data'])
        return data['description'][0]
    
def get_address(api_key, zpid):
    api_response = get_property_detail(api_key, zpid)    

    if api_response.status_code != 200: # Successful API call: Status 200
        return ""
    else:
        data = pd.json_normalize(api_response.json()['data'])
        return data['streetAddress'][0] + ' ' + data['zipcode'][0]

def address_to_zpid(api_key, address:str)->str:
    url = "https://app.scrapeak.com/v1/scrapers/zillow/zpidByAddress"
    
    # Regular expression pattern to extract street address, city, state, and zip code
    pattern = r'(?P<street>[0-9A-Za-z\s#.,-]+),\s*(?P<city>[A-Za-z\s]+),\s*(?P<state>[A-Za-z]{2})\s+(?P<zip>\d{5}(?:-\d{4})?)'

    # Match the pattern against the address
    match = re.match(pattern, address)

    if match:
        # Extract components
        street = match.group('street')
        city = match.group('city')
        state = match.group('state')
        zip_code = match.group('zip')

        querystring = {
        "api_key": api_key,
        "street":street,
        "city":city,
        "state":state,
        "zipcode":zip_code
        }

        api_response = requests.request("GET", url, params=querystring)
        data = pd.json_normalize(api_response.json()['data'])
        return data['zpid'][0]
    else:
        return "Please enter the address as: street, city, state, zipcode."


