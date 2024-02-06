from flask import Flask, render_template, request, flash
import pandas as pd
import sqlite3

from data_acquisition import get_listings, get_listings_gui
from create_database import create_database
from analysis import create_summary_table
from prediction import perform_prediction_gui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

api_key = "a9fef9b3-771c-4f18-87c1-aee712b66b4c"

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/home', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        url = request.form['url'] # Get from HTML form
        result = get_listings_gui(url, api_key)
        if not result:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired.")
        else:
            return render_template('home.html', result=result)
    return render_template('home.html')

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
        # Get from HTML form
        url = request.form['url']
        result = get_listings_gui(url, api_key)
        if not result:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired.")
            return render_template('analyze.html')        
        
        # Connect to the database
        database_connection = sqlite3.connect('zillow_listings.db')
        dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
        database_connection.close()
        
        summary_table = create_summary_table(dataframe).to_html()    
        return render_template('analyze.html', result=summary_table)
    return render_template('analyze.html')

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        # Get from HTML form
        url = request.form['url']
        result = get_listings_gui(url, api_key)
        if not result:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired.")
            return render_template('analyze.html')

        database_connection = sqlite3.connect('zillow_listings.db')
        dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
        database_connection.close()

        top_five_properties = perform_prediction_gui(dataframe)

        return render_template('predict.html', result=top_five_properties.to_html())
    return render_template('predict.html')

if __name__ == "__main__":
    app.run()