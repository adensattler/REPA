from flask import Flask, render_template, request, flash
import pandas as pd
import sqlite3
from config import API_KEY

from data_acquisition import get_listings, get_listings_gui, organize_property_details, get_description, get_address
from create_database import create_database
from analysis import create_summary_table
from prediction import perform_prediction_gui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/home', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        url = request.form['url'] # Get URL from HTML form
        result = get_listings_gui(url, API_KEY)
        
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
            create_database(selected_den_listings)
            return render_template('create.html', success_message = "Search was succesful!")
        except:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")
    return render_template('create.html')

@app.route('/analyze', methods=('GET', 'POST'))
def analyze():
    if request.method == 'POST':
        url = request.form['url'] # Get URL from HTML form
        result = get_listings_gui(url, API_KEY)
        
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
        url = request.form['url'] # Get URL from HTML form
        result = get_listings_gui(url, API_KEY)

        if not result:
            flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired.")
            return render_template('predict.html')

        database_connection = sqlite3.connect('zillow_listings.db')
        dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
        database_connection.close()

        top_five_properties = perform_prediction_gui(dataframe)

        return render_template('predict.html', result=top_five_properties.to_html())
    return render_template('predict.html')

def dict_to_html(data_dict):
    html = "<ul>"
    for key, value in data_dict.items():
        html += f"<li><strong>{key}:</strong> {value}</li>"
    html += "</ul>"
    return html

@app.route('/info', methods=('GET', 'POST'))
def info():
    if request.method == 'POST':
        zillow_id = request.form['zpid'] # Get Zillow ID from HTML form
        property_detail_dict, df_price_hist = organize_property_details(API_KEY, zillow_id)

        # make json files of the property details returned for usage by other routes
        data = pd.json_normalize(property_detail_dict)
        data.to_json('data.json')
        df_price_hist.to_json('hist.json')
        
        if not property_detail_dict:
            flash("Error: Please check that the Zillow ID is valid and try again. If the problem persists, check if your API key has expired for the month.")
        else:
            return render_template('info.html', dict=dict_to_html(property_detail_dict), df=df_price_hist.to_html())

    return render_template('info.html')

@app.route('/describe', methods=('GET', 'POST'))
def describe():
    if request.method == 'POST':
        zillow_id = request.form['zpid'] # Get Zillow ID from HTML form
        property_description = get_description(API_KEY, zillow_id)
        
        if not property_description:
            flash("Error: Please check that the Zillow ID is valid and try again. If the problem persists, check if your API key has expired for the month.")
        else:
            return render_template('describe.html', description=property_description)

    return render_template('describe.html')

# runs --info and subsequently runs --year on a given zpid
@app.route('/year', methods=('GET','POST'))
def year():
    # run --info with zpid obtained from form
    try:
        homeinfo(request.form['zpid'])
        # run --year after establishing --info
        data = pd.read_json('data.json')
        print(data['year built'][0][0])
        flash(data['year built'][0][0])
    except:
        print("Error: Please check that the ZPID is valid and try again. If the problem persists, check if your API key has expired for the month.")
    
    return render_template('year.html')

# runs --info and subsequently runs --nearby on a given zpid
@app.route('/nearby', methods=('GET','POST'))
def nearby():
    # run --info with zpid obtained from form
    try:
        homeinfo(request.form['zpid'])
        # run --nearby after establishing --info
        data = pd.read_json('data.json')
        for _ in range(len(data['nearby cities'][0])):
            print(data['nearby cities'][0][_])
            flash(data['nearby cities'][0][_])
    except:
        print("Error: Please check that the ZPID is valid and try again. If the problem persists, check if your API key has expired for the month.")

    return render_template('nearby.html')

# homeinfo function to reduce size of dependent functions (same functionality as --info)
def homeinfo(zpid):
    try:
        data, hist = organize_property_details(API_KEY, zpid)
        data = pd.json_normalize(data)
        data.to_json('data.json')
        hist.to_json('hist.json')
    except:
        print("Error: Please check that the ZPID is valid and try again. If the problem persists, check if your API key has expired for the month.")

@app.route('/addr', methods=('GET', 'POST'))
def addr():
    if request.method == 'POST':
        zillow_id = request.form['zpid'] # Get Zillow ID from HTML form
        property_address = get_address(API_KEY, zillow_id)
        
        if not property_address:
            flash("Error: Please check that the Zillow ID is valid and try again. If the problem persists, check if your API key has expired for the month.")
        else:
            return render_template('addr.html', address=property_address)

    return render_template('addr.html')

@app.route('/hist', methods=('GET', 'POST'))
def hist():
    if request.method == 'POST':

        try:
            hist_results = pd.read_json('hist.json')
            return render_template('hist.html', hist_results=hist_results.to_html())

        except:
            flash("Error: Please run --info command first")
        
    return render_template('hist.html')

if __name__ == "__main__":
    app.run()