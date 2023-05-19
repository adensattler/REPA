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
        api_key = "1d06fd5a-f8a8-4204-bf67-628653b0aa23"
        listing_url = args.url

        listing_response = get_listings(api_key, listing_url)

        # stores the columns we are interested in
        cols = ['zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.zipcode', 'beds', 'baths', 'area', 'hdpData.homeInfo.zestimate']

        # Takes all of the data and converts it into normalized, tabular data (.json_normalize)
        den_listings = pd.json_normalize(listing_response["data"]["cat1"]["searchResults"]["mapResults"])
        selected_den_listings = den_listings.loc[:, cols].dropna(thresh=7)

        create_database(selected_den_listings)

    if args.analyze:
        perform_analysis()

if __name__ == "__main__":
    main()