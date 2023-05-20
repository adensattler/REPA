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

def create_scatterplot(dataframe):
    fig = px.scatter(dataframe, x='area', y=['zestimate', 'price'],
                     color_discrete_sequence=["blue", "red"],
                     title="House value vs. Area")
    fig.show()


def create_pie_chart_house_types(dataframe):
    house_types = dataframe['house_type'].value_counts()
    total_count = house_types.sum()
    proportions = house_types / total_count

    fig = px.pie(
        values=proportions,
        names=house_types.index,
        title='Ratio of House Types'
    )
    fig.show()
    

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

    # Close the database connection
    conn.close()