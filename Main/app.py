from flask import Flask, render_template, request, flash
import pandas as pd
import sqlite3

from data_acquisition import get_listings
from create_database import create_database
from analysis import create_summary_table
from prediction import load_linear_regression_model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

api_key = "a9fef9b3-771c-4f18-87c1-aee712b66b4c"

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    # if a post request is made lets check out what was posted!
    if request.method == 'POST':
        # get the url from the form that was submitted
        url = request.form['url']

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
    return render_template('create.html')

@app.route('/analyze', methods=('GET', 'POST'))
def analyze():
    if request.method == 'POST':
        # get the url from the form that was submitted
        url = request.form['url']

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

            # Connect to the database
            database_connection = sqlite3.connect('zillow_listings.db')

            # Execute the query and convert results to a DataFrame
            df = pd.read_sql_query("SELECT * FROM listings", database_connection)
            summary_table = create_summary_table(df).to_html()    
            database_connection.close()
            return render_template('analyze.html', result=summary_table)
        except:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")
    return render_template('analyze.html')

def perform_prediction(df):
    denver_model = load_linear_regression_model('denver_model.pickle')

    # Retrieve the necessary attributes for prediction
    features = df[['num_beds', 'num_baths', 'area', 'tax_ass_val', 'latitude', 'longitude']]

    # Make predictions using the models
    denver_predictions = denver_model.predict(features)

    # Calculate the difference between predicted prices and actual prices
    df['denver_predicted'] = denver_predictions
    df['denver_difference'] = df['denver_predicted'] - df['price']
    
    # Sort the houses based on the difference in descending order
    df_sorted = df.sort_values('denver_difference', ascending=False)

    # Return the top investments
    return df_sorted[['zillow_ID', 'price', 'denver_predicted', 'denver_difference']].head(), df

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        # get the url from the form that was submitted
        url = request.form['url']
        listing_url = url
        listing_response = None

        try:
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

            database_connection = sqlite3.connect('zillow_listings.db')

            # Execute the query and convert results to a DataFrame
            df = pd.read_sql_query("SELECT * FROM listings", database_connection)
            database_connection.close()

            # Perform prediction and obtain the updated dataframe
            top_five_properties, df = perform_prediction(df)

            return render_template('predict.html', result=top_five_properties.to_html())
        except:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")
    return render_template('predict.html')

if __name__ == "__main__":
    app.run()