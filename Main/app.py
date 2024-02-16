from flask import Flask, render_template, request, url_for, flash, redirect
import pandas as pd
import sqlite3
from werkzeug.exceptions import abort
from config import API_KEY

from data_acquisition import get_listings, get_listings_gui, organize_property_details, get_description, get_address, save_api_response, get_property_detail
from database import *
from analysis import create_summary_table
from prediction import perform_prediction_gui
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

create_database()

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

# Helper function
def list_to_html(data_list):
    html = "<ul>\n"
    for item in data_list:
        html += f"  <li>{item}</li>\n"
    html += "</ul>"
    return html

@app.route('/home', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        url = request.form['url'] # Get URL from HTML form
        result = get_listings_gui(url, API_KEY)
        
        if not result:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired.")
        else:
            # Connect to the database
            database_connection = sqlite3.connect('zillow_listings.db')
            dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
            database_connection.close()
            
            top_five_properties = perform_prediction_gui(dataframe)
            zillow_id_list = top_five_properties['zillow_ID'].to_list()
            print(zillow_id_list)
            address_list = []
            for zillow_id in zillow_id_list:
                address_list.append(get_address(API_KEY, zillow_id))

            return render_template('home.html', result=list_to_html(address_list))
    return render_template('home.html')

@app.route('/analyze', methods=('GET', 'POST'))
def analyze():
    if request.method == 'POST':
        try:
            database_connection = sqlite3.connect('zillow_listings.db')
            dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
            database_connection.close()
            
            summary_table = create_summary_table(dataframe).to_html()    
            return render_template('analyze.html', result=summary_table)
        except:
            flash("zillow_listings.db is empty. Please run --url first.")
    return render_template('analyze.html')

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        try:
            database_connection = sqlite3.connect('zillow_listings.db')
            dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
            database_connection.close()

            top_five_properties = perform_prediction_gui(dataframe)
            return render_template('predict.html', result=top_five_properties.to_html())
        except:
            flash("zillow_listings.db is empty. Please run --url first.")
    return render_template('predict.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    # if a post request is made lets check out what was posted!
    if request.method == 'POST':
        # get the url from the form that was submitted
        url = request.form['url']

        try:
            listing_url = url

            listing_response = get_listings(API_KEY, listing_url)

            # stores the columns we are interested in
            columns = [
                'zpid', 'hdpData.homeInfo.price', 'hdpData.homeInfo.bedrooms', 'hdpData.homeInfo.bathrooms', 'area',
                'hdpData.homeInfo.zipcode', 'hdpData.homeInfo.livingArea', 'hdpData.homeInfo.homeType', 'hdpData.homeInfo.zestimate', 'hdpData.homeInfo.city', 'hdpData.homeInfo.latitude', 'hdpData.homeInfo.longitude',
                'hdpData.homeInfo.taxAssessedValue'
            ]

            # Takes all of the data and converts it into normalized, tabular data (.json_normalize)
            den_listings = pd.json_normalize(listing_response["data"]["cat1"]["searchResults"]["mapResults"])
            selected_den_listings = den_listings.loc[:, columns].dropna(thresh=13)
            fill_database(selected_den_listings)
            return render_template('create.html', success_message = "Search was succesful!")
        except:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")
    return render_template('create.html')

# NEW ROUTES FOR VERSION 2 OF THE APP
# --------------------------------------------------------------------------------------------------------

# ROUTE TO THE PROPERTY SEARCH PAGE
@app.route('/property_home', methods=('GET', 'POST'))
def property_home():
    if request.method == 'POST':
        zpid = request.form['zpid'] # Get Zillow ID from HTML form

        if not zpid:
            flash('zillow id is required!')
        else:
            # Retrieve raw property data from the API
            data = get_property_detail(API_KEY, zpid)
            
            # Add property data to the database
            insert_property_db(zpid, data.text)

            # Redirect the user to the property page on submission
            return redirect(url_for('property', zpid=zpid))

    # Retrieve property search history from the database
    properties = get_prop_search_history()

    # Pass the properties to the html page as a list of dictionaries!
    return render_template('property_home.html', properties=properties)

# ROUTE TO A SPECIFIC PROPERTY PAGE
@app.route('/property/<int:zpid>')
def property(zpid):
    property = get_property_from_db(zpid)
    return render_template('property.html', property=property)


if __name__ == "__main__":
    app.run()
