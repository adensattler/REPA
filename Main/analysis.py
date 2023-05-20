import sqlite3
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def create_summary_table(dataframe):
    summary_data = {
        'Metric': ['Minimum', 'Maximum', 'Mean', 'Median'],
        'Price': [dataframe['price'].min(), dataframe['price'].max(), dataframe['price'].mean(), dataframe['price'].median()],
        'Size': [dataframe['area'].min(), dataframe['area'].max(), dataframe['area'].mean(), dataframe['area'].median()],
        'Bedrooms': [dataframe['no_of_beds'].min(), dataframe['no_of_beds'].max(), dataframe['no_of_beds'].mean(), dataframe['no_of_beds'].median()],
        'Bathrooms': [dataframe['no_of_baths'].min(), dataframe['no_of_baths'].max(), dataframe['no_of_baths'].mean(), dataframe['no_of_baths'].median()]
    }
    
    summary_table = pd.DataFrame(summary_data)
    summary_table = summary_table.set_index('Metric')
    
    return summary_table

def perform_analysis():
    # Connect to the database
    conn = sqlite3.connect('zillow_listings.db')

    # Execute the query and convert results to a DataFrame
    df = pd.read_sql_query("SELECT * FROM listings", conn)

    # Create the scatter plot using plotly.express
    fig = px.scatter(df, x=df['area'], y=[df['zestimate'], df['price']],
                     color_discrete_sequence=["blue", "red"],
                     title="House value vs. Area")
    fig.show()

    # Create the summary table
    summary_table = create_summary_table(df)
    print(summary_table)
    # Close the database connection
    conn.close()

