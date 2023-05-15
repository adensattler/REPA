import pandas as pd
import numpy as np
import plotly.express as px
import requests
import warnings

pd.set_option('display.max_rows', None)

def get_property_detail(api_key, zpid):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/property"

    querystring = {
        "api_key": api_key,
        "zpid":zpid
    }

    return requests.request("GET", url, params=querystring)

# api key from scrapeak to use the zillow API
api_key = "1d06fd5a-f8a8-4204-bf67-628653b0aa23"


# property unique id
zpid = "13314727"

# get property detail
prop_detail_response = get_property_detail(api_key, zpid)

# view all keys
print(prop_detail_response.json().keys())

# check if request is successful
print("Request success:", prop_detail_response.json()["is_success"])

df_prop = pd.json_normalize(prop_detail_response.json()['data'])

# view price history
df_price_hist = pd.DataFrame(df_prop["priceHistory"].iloc[0])
print(df_price_hist)