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
    parser.add_argument("--comp", action="store_true", help="Compare to nearby houses")
    parser.add_argument("--nearby", action="store_true", help="Get nearby cities")
    parser.add_argument("--hist", action="store_true", help="Get price history")
    parser.add_argument("--year", action="store_true", help="Get year built")

    args = parser.parse_args()

    if args.url:
        try:
            api_key = "00b71f28-feee-48d9-b482-c06247c6f6cf"
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
        except:
            print("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")

    if args.analyze:
        try:
            perform_analysis()
        except:
            print("Error: Please run --url command first")
        
    if args.predict:
        try:
            predict()
        except:
            print("Error: Please run --url command first")

    if args.info:
        try:
            api_key = "e73c0de1-9ae1-493c-9d3a-b3d6875b6eed"
            zpid = args.info
            data, hist = organize_property_details(api_key, zpid)
            data = pd.json_normalize(data)
            data.to_json('data.json')
            hist.to_json('hist.json')
        except:
            print("Error: Please check that the ZPID is valid and try again. If the problem persists, check if your API key has expired for the month.")
    
    if args.addr:
        try:
            data = pd.read_json('data.json')
            print(data['street address'][0][0])
        except:
            print("Error: Please run --info command first")
    if args.describe:
        try:
            data = pd.read_json('data.json')
            print(data['description'][0][0])
        except:
            print("Error: Please run --info command first")
    if args.school:
        try:
            data = pd.read_json('data.json')
            for _ in range(len(data['schools'][0])):
                print(data['schools'][0][_])
                print('\n')
        except:
            print("Error: Please run --info command first")
    if args.comp:
        try:
            data = pd.read_json('data.json')
            for _ in range(len(data['comps'][0])):
                print(data['comps'][0][_])
        except:
            print("Error: Please run --info command first")
    if args.nearby:
        try:
            data = pd.read_json('data.json')
            for _ in range(len(data['nearby cities'][0])):
                print(data['nearby cities'][0][_])
        except:
            print("Error: Please run --info command first")
    if args.hist:
        try:
            data = pd.read_json('hist.json')
            print(data)
        except:
            print("Error: Please run --info command first")

    if args.year:
        try:
            data = pd.read_json('data.json')
            print(data['year built'][0][0])
        except:
            print("Error: Please run --info command first")

if __name__ == "__main__":
    main()
