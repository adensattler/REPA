import sqlite3
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_rows', None)

def load_linear_regression_model(filepath):
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

def perform_prediction(df):
    # Load the linear regression models
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
    
     # Save the predicted properties as a CSV file
    df_sorted.to_csv('predictions.csv', index=False)

    # Print the top investments
    print("Denver Area - Best Value Houses:")
    print(df_sorted[['zillow_ID', 'price', 'denver_predicted', 'denver_difference']].head())
    print()

    return df

def scatter_plot_actual_predicted(df):
    plt.scatter(df['price'], df['denver_predicted'], color='blue', label='Predicted')
    plt.scatter(df['price'], df['price'], color='red', label='Actual')
    plt.xlabel('Actual House Price')
    plt.ylabel('Predicted House Price')
    plt.title('Actual vs Predicted House Prices')
    plt.legend()
    plt.show()

def residual_plot(df):
    plt.scatter(df['price'], df['denver_difference'], color='blue')
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel('Actual House Price')
    plt.ylabel('Residuals')
    plt.title('Residual Plot - Denver Area')
    plt.show()

def box_plot_house_types(df):
    sns.boxplot(data=df, x='house_type', y='denver_difference')
    plt.xlabel('House Type')
    plt.ylabel('Price Difference')
    plt.title('Price Difference by House Type')
    plt.show()

def violin_plot_num_bedrooms(df):
    sns.violinplot(data=df, x='num_beds', y='denver_difference')
    plt.xlabel('Number of Bedrooms')
    plt.ylabel('Price Difference')
    plt.title('Price Difference by Number of Bedrooms')
    plt.show()

def histogram_price_difference(df):
    plt.hist(df['denver_difference'], bins=20, color='skyblue')
    plt.xlabel('Price Difference')
    plt.ylabel('Frequency')
    plt.title('Distribution of Price Difference')
    plt.show()

def create_predicted_heat_map(df):
    # Create a map centered on the average latitude and longitude of the data
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    heat_map = folium.Map(location=map_center, zoom_start=12)

    # Convert the data to list of tuples (latitude, longitude, value)
    data = list(zip(df['latitude'], df['longitude'], df['denver_difference']))

    # Create a HeatMap layer using the data
    heat_layer = HeatMap(data, radius=15)
    heat_map.add_child(heat_layer)

    # Add title to the map
    folium.map.Marker(
        map_center,
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html=f'<div style="font-weight: bold; font-size: 16px;">{"Price Difference Heat Map"}</div>',
            )
        ).add_to(heat_map)

    # Save the map as an HTML file
    heat_map.save("price_difference_heatmap.html")
    
def visualize_prediction(df):
    scatter_plot_actual_predicted(df)
    residual_plot(df)
    box_plot_house_types(df)
    violin_plot_num_bedrooms(df)
    histogram_price_difference(df)
    create_predicted_heat_map(df)

def predict():
    # Connect to the database
    conn = sqlite3.connect('zillow_listings.db')

    # Execute the query and convert results to a DataFrame
    df = pd.read_sql_query("SELECT * FROM listings", conn)

    # Close the database connection
    conn.close()

    # Perform prediction and obtain the updated dataframe
    df = perform_prediction(df)

    # Visualize the prediction using various graphs
    visualize_prediction(df)


