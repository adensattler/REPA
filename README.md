# real-estate-price-analysis
Real Estate Price Prediction and Investment Analysis

## Client

Leo Dixon, Executive MBA PhD Candidate, Adjunct Faculty, Daniels College of Business, University of Denver, leo.dixon@du.edu
Description

## Description

The aim of this project is to develop a machine learning model that predicts real estate prices and identifies potentially profitable investment opportunities in the housing market using historical and current data of the real estate market.

## Getting the Program to work
1. If you haven't already, install the latest version of Python. You can install it from here: [website](https://www.python.org/downloads/)
2. In a terminal window, run the following command lines to install the necessary dependencies for the program:
`pip install sqlite3`
`pip install pandas`
`pip install plotly`
`pip install seaborn`
`pip install matplotlib`
`pip install folium`
`pip install requests`
3. Clone the repository onto your local machine. Choose a directory that you plan to have the program in, open a terminal window on that directory, and run the following command line to clone:
`git clone https://github.com/dussec/real-estate-price-analysis.git'
4. Go to the Zillow website ([website](https://www.zillow.com/)) and search for homes (for sale) in the Denver. Try to include a variety of areas (Aurora, Centennial, etc) and a broad criteron for a large dataset. Once you're done with the search, copy the link in the address bar.
If you wish, you can use this link already provided in the 'zillow_example.txt' file under the 'Examples' folder.

5. Open a new terminal window on the folder 'Main'.  


## Commands 
### --url 
Command: 'python main.py --url [zillow search url]`
Purpose: It will create a SQLite database of listings from the search url you obtained previously. The url is a required argument for the command.
Expected output: 'zillow_listings.db' should be created in the same directory ('Main' folder). And, a list of keys and the number of properties retrieved should be be shown. For example:
```
dict_keys(['user', 'mapState', 'regionState', 'searchPageSeoObject', 'requestId', 'cat1', 'categoryTotals'])
Count of properties: 1969
```

Note: If this command does not work, please use the provided 'zillow_listings.db' in the 'Examples' folder of the repository. Move it to the 'Main' folder on your local machine.
Note: In order to run the other two commands, tt is important to have 'zillow_listings.db' in the 'Main' folder. Otherwise, it those commands will note work.

### --analyze
Command: 'python main.py --analyze`
Purpose: It will conduct Exploratory Data Analysis (EDA) on the properties off the database. 
Expected output: 
*a summary table to the terminal.
*a variety of graphs (should be 6) that will appear in a seperate popup window (the next graph will not be shown unless you exit out of the window of the current graph).
*a heat geographic heat map (should appear as heatmap.html) of current prices that will be saved to the current directory (inside 'Main'). You can open it in your browser to interact with it.

### --predict 
Command: 'python main.py --predict'
Purpose: It will use a linear regression machine learning model create predicted prices of the properties off the database and compare it with the actual price to determine which properties are undervalued (ideal for investment). 
Expected output:
*a list of 5 properties with the best value. It will have their Zillow ID, actual price, predicted price, and the difference between the two. It will be shown in the terminal.
*a variety of graphs (should be 5) that will appear in a seperate popup window (the next graph will not be shown unless you exit out of the window of the current graph).
*a heat geographic heat map (should appear as price_difference_heatmap.html) that will be saved to the current directory (inside 'Main'). You can open it in your browser to interact with it.
## Help
If the the last two commands do not work, or any other issue arises, please let us know.
