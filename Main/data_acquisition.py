import requests
import pandas as pd

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
        return prop_detail_dict
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
