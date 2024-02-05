from flask import Flask, render_template, request, flash
import pandas as pd

from data_acquisition import get_listings
from data_acquisition import organize_property_details
from create_database import create_database
from analysis import perform_analysis
from prediction import predict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    # if a post request is made lets check out what was posted!
    if request.method == 'POST':
        # get the url from the form that was submitted
        url = request.form['url']
        print(url)

        # check that input is not empty
        # if "https://www.zillow.com/" not in url:
        #     flash('URL is required!')
        # else:
        try:
            api_key = "a9fef9b3-771c-4f18-87c1-aee712b66b4c"
            listing_url = url

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
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")
            print("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")



    return render_template('create.html')


@app.route('/predict', methods=('GET', 'POST'))
def predictPage():
    if request.method == 'POST':
        try:
           predict() 
        except:
            flash("Error: please make sure that you have already created the database")
            print("Error: please make sure that you have already created the database")
    return render_template('predict.html')

if __name__ == "__main__":
    app.run()
