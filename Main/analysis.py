import sqlite3
import pandas as pd
import plotly.express as px

def perform_analysis():
    # Connect to the database
    conn = sqlite3.connect('zillow_listings.db')

    # execute the query and convert results to a dataframe
    df = pd.read_sql_query("SELECT area, zestimate, price FROM listings", conn)

    fig = px.scatter(df, x=df['area'], y=[df['zestimate'], df['price']], 
                     color_discrete_sequence=["blue", "red"], 
                     title="House value vs. Area")
    fig.show()

    # Close the database connection
    conn.close()
