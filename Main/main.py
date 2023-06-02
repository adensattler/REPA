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
    info_parser = parser.add_argument("--info", help="Print House Information")
    info_group = parser.add_mutually_exclusive_group(required=True)
    info_group.add_argument("--addr", action='store_true', help="Get street address")
    info_group.add_argument("--describe", action='store_true', help="Get house description")
    info_group.add_argument("--school", action='store_true', help="Get school information")
    info_group.add_argument("--comp", action='store_true', help="Compare to nerby houses")
    info_group.add_argument("--nearby", action='store_true', help="Get nearby cities")
    info_group.add_argument("--hist", action='store_true', help="Get price history")
    info_group.add_argument("--year", action='store_true', help="Get year built")

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
        pd.set_option('display.max_colwidth', None)
        api_key = "bead7c5a-3ccb-4a9f-b2d2-efc02707840a"
        zpid = args.info
        data = organize_property_details(api_key, zpid)
        data = pd.json_normalize(data)
        # print(data)
        if args.addr:
            print(data['street address'])
        elif args.describe:
            print(data['description'][0][0])
        elif args.school:
            for _ in range(len(data['schools'][0])):
                print(data['schools'][0][_])
                print('\n')
        elif args.comp:
            for _ in range(len(data['comps'][0])):
                print(data['comps'][0][_])
        elif args.nearby:
            for _ in range(len(data['nearby cities'][0])):
                print(data['nearby cities'][0][_])
        elif args.hist:
            for _ in range(len(data['price history'])):
                print(data['price history'][0][_])
        elif args.year:
            print(data['year built'][0][0])

if __name__ == "__main__":
    main()
