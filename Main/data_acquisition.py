import requests

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
