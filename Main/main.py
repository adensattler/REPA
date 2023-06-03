import sys
import argparse
import pandas as pd
from data_acquisition import get_listings
from data_acquisition import organize_property_details
from create_database import create_database
from analysis import perform_analysis
from prediction import predict

def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="Real Estate Analysis Program")
    parser.add_argument("--url", help="Zillow search URL")
    parser.add_argument("--analyze", action="store_true", help="Perform analysis")
    parser.add_argument("--predict", action="store_true", help="Perform prediction")
    parser.add_argument("--info", help="Print House Information")
    parser.add_argument("--addr", action="store_true", help="Get street address")
    parser.add_argument("--describe", action="store_true", help="Get house description")
    parser.add_argument("--school", action="store_true", help="Get school information")
    parser.add_argument("--comp", action="store_true", help="Compare to nerby houses")
    parser.add_argument("--nearby", action="store_true", help="Get nearby cities")
    parser.add_argument("--hist", action="store_true", help="Get price history")
    parser.add_argument("--year", action="store_true", help="Get year built")

    args = parser.parse_args()

    if args.url:
        api_key = "20f2b911-a35e-4fdb-b54a-a466f52098a0"
        listing_url = args.url

        listing_response = get_listings(api_key, listing_url)

        # stores the columns we are interested in
        columns = [
            'zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.bedrooms', 'hdpData.homeInfo.bathrooms', 'area',
            'hdpData.homeInfo.zipcode', 'hdpData.homeInfo.livingArea', 'hdpData.homeInfo.homeType', 'hdpData.homeInfo.zestimate', 'hdpData.homeInfo.city', 'hdpData.homeInfo.latitude', 'hdpData.homeInfo.longitude', 
            'hdpData.homeInfo.taxAssessedValue'	
        ]

        # Takes all of the data and converts it into normalized, tabular data (.json_normalize)
        den_listings = pd.json_normalize(listing_response["data"]["cat1"]["searchResults"]["mapResults"])
        selected_den_listings = den_listings.loc[:, columns].dropna(thresh=13)
        create_database(selected_den_listings)

    if args.analyze:
        perform_analysis()
        
    if args.predict:
        predict()

    if args.info:
        api_key = "bead7c5a-3ccb-4a9f-b2d2-efc02707840a"
        zpid = args.info
        data = organize_property_details(api_key, zpid)
        data = pd.json_normalize(data)
        data.to_json('data.json')
    
    if args.addr:
        data = pd.read_json('data.json')
        print(data['street address'][0][0])
    if args.describe:
        data = pd.read_json('data.json')
        print(data['description'][0][0])
    if args.school:
        data = pd.read_json('data.json')
        for _ in range(len(data['schools'][0])):
            print(data['schools'][0][_])
            print('\n')
    if args.comp:
        data = pd.read_json('data.json')
        for _ in range(len(data['comps'][0])):
            print(data['comps'][0][_])
    if args.nearby:
        data = pd.read_json('data.json')
        for _ in range(len(data['nearby cities'][0])):
            print(data['nearby cities'][0][_])
    if args.hist:
        data = pd.read_json('data.json')
        for _ in range(len(data['price history'])):
            print(data['price history'][0][_])
    if args.year:
        data = pd.read_json('data.json')
        print(data['year built'][0][0])

if __name__ == "__main__":
    main()
