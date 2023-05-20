import sys
import argparse
import pandas as pd
from data_acquisition import get_listings
from create_database import create_database
from analysis import perform_analysis

def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="Real Estate Analysis Program")
    parser.add_argument("--url", help="Zillow search URL")
    parser.add_argument("--analyze", action="store_true", help="Perform analysis")

    args = parser.parse_args()

    if args.url:
        api_key = "20f2b911-a35e-4fdb-b54a-a466f52098a0"
        listing_url = args.url

        listing_response = get_listings(api_key, listing_url)

        # stores the columns we are interested in
        columns = [
            'zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.bedrooms', 'hdpData.homeInfo.bathrooms', 'area',
            'hdpData.homeInfo.zipcode', 'hdpData.homeInfo.livingArea', 'hdpData.homeInfo.homeType', 'hdpData.homeInfo.zestimate', 'hdpData.homeInfo.city', 'hdpData.homeInfo.latitude', 'hdpData.homeInfo.longitude'	
        ]

        # Takes all of the data and converts it into normalized, tabular data (.json_normalize)
        den_listings = pd.json_normalize(listing_response["data"]["cat1"]["searchResults"]["mapResults"])
        selected_den_listings = den_listings.loc[:, columns].dropna(thresh=12)
        create_database(selected_den_listings)

    if args.analyze:
        perform_analysis()

if __name__ == "__main__":
    main()
