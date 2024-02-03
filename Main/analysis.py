import sqlite3
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import folium
from folium.plugins import HeatMap

def create_summary_table(dataframe):
    summary_data = {
        'Metric': ['Minimum', 'Maximum', 'Mean', 'Median'],
        'Price': [dataframe['price'].min(), dataframe['price'].max(), dataframe['price'].mean(), dataframe['price'].median()],
        'Size': [dataframe['area'].min(), dataframe['area'].max(), dataframe['area'].mean(), dataframe['area'].median()],
        'Bedrooms': [dataframe['num_beds'].min(), dataframe['num_beds'].max(), dataframe['num_beds'].mean(), dataframe['num_beds'].median()],
        'Bathrooms': [dataframe['num_baths'].min(), dataframe['num_baths'].max(), dataframe['num_baths'].mean(), dataframe['num_baths'].median()]
    }
    
    summary_table = pd.DataFrame(summary_data)
    summary_table = summary_table.set_index('Metric')
    
    return summary_table

def create_scatterplot(dataframe):
    plt.scatter(dataframe['area'], dataframe['zestimate'], color='blue', label='zestimate', alpha=0.5, s=10)
    plt.scatter(dataframe['area'], dataframe['price'], color='red', label='price', alpha=0.8, s=10)
    plt.xlabel('Area')
    plt.ylabel('House Value')
    plt.title('House value vs. Area')
    plt.legend()
    plt.show()

def create_pie_chart_house_types(dataframe):
    house_types = dataframe['house_type'].value_counts()
    total_count = house_types.sum()
    proportions = house_types / total_count

    plt.pie(proportions, labels=house_types.index, autopct='%1.1f%%')
    plt.title('Ratio of House Types')
    plt.show()
    
    

def create_bar_chart_average_price(dataframe):
    avg_prices = dataframe.groupby('zipcode')['price'].mean().reset_index()

    # Filter out zip codes with no mean value
    avg_prices = avg_prices[~avg_prices['price'].isnull()]

    plt.figure(figsize=(12, 6))
    sns.barplot(x='zipcode', y='price', data=avg_prices)
    plt.xlabel('Zipcode')
    plt.ylabel('Average Price')
    plt.title('Average Price per Zipcode')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def create_boxplot_prices_per_city(dataframe):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='city', y='price', data=dataframe)
    plt.xlabel('City')
    plt.ylabel('Price')
    plt.title('Prices per City')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
def create_bar_chart_average_price_house_type(dataframe):
    avg_prices = dataframe.groupby('house_type')['price'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lavender', 'gold']
    ax = plt.gca()

    avg_prices.plot(kind='bar', x='house_type', y='price', color=colors, ax=ax, legend=False)
    plt.xlabel('House Type')
    plt.ylabel('Average Price ($)')
    plt.title('Average Price per House Type')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
def create_correlation_matrix(dataframe):
    attributes = ['price', 'area', 'living_area', 'num_beds', 'num_baths', 'zestimate']
    correlation_matrix = dataframe[attributes].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Between Important Attributes')
    plt.show()
    
def create_price_heatmap(dataframe):
    # Create a map centered around the average latitude and longitude of the listings
    average_lat = dataframe['latitude'].mean()
    average_lon = dataframe['longitude'].mean()
    map_heat = folium.Map(location=[average_lat, average_lon], zoom_start=12)

    # Create a HeatMap layer using the house locations and prices
    heat_data = [[row['latitude'], row['longitude'], row['price']] for _, row in dataframe.iterrows()]
    HeatMap(heat_data).add_to(map_heat)

    map_heat.save('heatmap.html')


def perform_analysis():
    # Connect to the database
    conn = sqlite3.connect('zillow_listings.db')

    # Execute the query and convert results to a DataFrame
    df = pd.read_sql_query("SELECT * FROM listings", conn)

    # Create the scatter plot using Plotly Express
    create_scatterplot(df)

    # Create the summary table
    summary_table = create_summary_table(df)
    print(summary_table)

    # Create the pie chart for house types
    create_pie_chart_house_types(df)
    
    # Create the bar chart for average price per zipcode
    create_bar_chart_average_price(df)
    
    # Create the boxplot for prices per city
    create_boxplot_prices_per_city(df)
    
    # Create the bar chart for average price per house type
    create_bar_chart_average_price_house_type(df)
    
    # Create the heatmap for attribute correlation
    create_correlation_matrix(df)
    
    create_price_heatmap(df)
    
    # Close the database connection
    conn.close()



