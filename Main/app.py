from flask import Flask, render_template, request, url_for, flash, redirect
from flask_caching import Cache
import pandas as pd
import sqlite3
from werkzeug.exceptions import abort
from config import API_KEY
from data_acquisition import *
from database import DatabaseManager
from analysis import create_summary_table
from prediction import perform_prediction_gui
from assistant import generate_response
import json
from db_debug import resetDB
import evaluationFunctions
from urllib.parse import quote

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

database = DatabaseManager('zillow_listings.db')
database.create_database()

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

# NEW ROUTES FOR VERSION 2 OF THE APP
# --------------------------------------------------------------------------------------------------------
@app.route('/listings-search', methods=('GET', 'POST'))
def listings_search():
    # if a post request is made lets check out what was posted!
    if request.method == 'POST':
        if "url" in request.form:
                
            # get the url from the form that was submitted
            url = request.form['url']
            try:
                listing_url = url

                print(get_listings_gui(listing_url, API_KEY))

                return render_template('listings_search.html', success_message = "Search was successful!")
            except:
                flash("Error: Please check that the URL is valid and try again. If the problem persists, check if your API key has expired for the month.")

        elif "predict" in request.form:
            try:
                database_connection = sqlite3.connect('zillow_listings.db')
                dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
                database_connection.close()

                top_five_properties = perform_prediction_gui(dataframe)
                return render_template('listings_search.html', predict_result=top_five_properties.to_html())
            except:
                flash("zillow_listings.db is empty. Please enter url first.")

        elif "analyze" in request.form:
            try:
                database_connection = sqlite3.connect('zillow_listings.db')
                dataframe = pd.read_sql_query("SELECT * FROM listings", database_connection)
                database_connection.close()
                
                summary_table = create_summary_table(dataframe).to_html()    
                return render_template('listings_search.html', analyze_result=summary_table)
            except:
                flash("zillow_listings.db is empty. Please enter url first.")
            
    return render_template('listings_search.html')

# ROUTE TO THE PROPERTY SEARCH PAGE
@app.route('/propertysearch', methods=('GET', 'POST'))
def property_search():
    database = DatabaseManager('zillow_listings.db')
    if request.method == 'POST':
        zpid = request.form['search_term'] # Get Zillow ID or address from HTML form
        
        # If searching by address
        if not zpid.isdigit():
            zpid = address_to_zpid(API_KEY, address=zpid)
            if not zpid.isdigit():
                flash("Please enter the address as: street, city, state, zipcode.")

        # Retrieve raw property data from the API
        data = get_property_detail(API_KEY, zpid)

        #Check to make sure api returns a property
        if json.loads(data.text)["data"]:
            
            # Add property data to the database
            database.insert_property_db(zpid, data.text)
            try:
                url = database.add_nearby_homes(zpid)
                print(get_listings_gui(url,API_KEY))
                evaluationFunctions.PriceRelativeArea(zpid, database.get_value_from_property_db(zpid,"price"),database.get_value_from_property_db(zpid,"zipcode"))
            except:
                print("nearby homes already in DB")

            # Redirect the user to the property page on submission
            return redirect(url_for('property', zpid=zpid))
        else:
            flash('Please enter a valid Zillow ID')

    # Retrieve property search history from the database
    
    recent_searches = cache.get('recent_searches') or []
    properties = database.get_prop_search_history(recent_searches)
    # properties = database.get_prop_search_history()

    favorite_properties = database.get_favorite_properties()

    # Pass the properties to the html page as a list of dictionaries!
    return render_template('property_search.html', properties=properties, favorites=favorite_properties)

# ROUTE TO A SPECIFIC PROPERTY PAGE
@app.route('/property/<int:zpid>')
def property(zpid):
    database = DatabaseManager('zillow_listings.db')
    property = database.get_property_from_db(zpid)

    #Caching:
    recent_searches = cache.get('recent_searches') or []

    if zpid in recent_searches:
        recent_searches.remove(zpid)
    recent_searches.insert(0, zpid)
    recent_searches = recent_searches[:4]
    #Assign it to the cache
    cache.set('recent_searches', recent_searches)
    print(recent_searches)

    # Image URLs stored as list JSON-encoded in database
    images_json = database.get_images_from_property_db(zpid)
    image_urls = json.loads(images_json) if images_json else []

    # Properly encode each URL in the images list
    encoded_images = [quote(url, safe=':/') for url in image_urls]

    # rawjson = json.loads(database.get_JSON(zpid))
    # return render_template('property.html', property=property, rawjson=rawjson)
    return render_template('property.html', property=property, images=encoded_images)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    zpid = request.form.get('zpid')
    if zpid:
        try:
            # Add the property to the favorites list in the database
            database.add_to_favorites(zpid)
            flash('Property added to favorites successfully.', 'success')
        except Exception as e:
            flash('An error occurred while adding to favorites: ' + str(e), 'error')
    else:
        flash('Invalid property ID.', 'error')
    return redirect(url_for('property_search'))

@app.route('/reset')
def reset():
    if request.method == "GET":
        resetDB()
        database = DatabaseManager('zillow_listings.db')
        database.create_database()
        flash('Database has been reset')
        return redirect(url_for('property_search'))
     
    return redirect(url_for('property_search'))

@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    zpid = request.form.get('zpid')
    if zpid:
        try:
            database.remove_from_favorites(zpid)
            flash('Property removed from favorites successfully.', 'success')
        except Exception as e:
            flash('An error occurred while removing from favorites: ' + str(e), 'error')
    else:
        flash('Invalid property ID.', 'error')
    return redirect(url_for('property_search'))

@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    zpid = request.form.get('zpid')
    if zpid:
        try:
            if database.is_favorite(zpid):
                database.remove_from_favorites(zpid)
                flash('Property removed from favorites successfully.', 'success')
            else:
                database.add_to_favorites(zpid)
                flash('Property added to favorites successfully.', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
    else:
        flash('Invalid property ID.', 'error')
    return redirect(request.referrer or url_for('property_search'))

@app.route('/get')
def get_assistant_response():
    input = request.args.get('msg')
    zpid = request.args.get('zpid')
    response = generate_response(input, zpid=zpid)
    return response

if __name__ == "__main__":
    app.run()


