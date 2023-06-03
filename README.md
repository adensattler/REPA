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
`pip install scikit-learn`

3. Clone the repository onto your local machine. Choose a directory that you plan to have the program in, open a terminal window on that directory, and run the following command line to clone:
`git clone https://github.com/dussec/real-estate-price-analysis.git`
4. Go to the Zillow website ([website](https://www.zillow.com/)) and search for homes (for sale) in the Denver. Try to include a variety of areas (Aurora, Centennial, etc) and a broad criteron for a large dataset. Once you're done with the search, copy the link in the address bar. If you wish, you can use this link already provided in the `zillow_example.txt` file under the 'Examples' folder.

5. Open a new terminal window on the folder `Main`.  


## Commands 
### --url 
Command: `python main.py --url [zillow search url]`

Purpose: It will create a SQLite database of listings from the search url you obtained previously. The url is a required argument for the command.

Expected output: 'zillow_listings.db' should be created in the same directory (`Main` folder). And, a list of keys and the number of properties retrieved should be be shown. For example:
```
dict_keys(['user', 'mapState', 'regionState', 'searchPageSeoObject', 'requestId', 'cat1', 'categoryTotals'])
Count of properties: 1969
```

Note: If this command does not work, please use the provided `zillow_listings.db` in the `Examples` folder of the repository. Move it to the `Main` folder on your local machine.

Note: In order to run the other two commands, it is important to have `zillow_listings.db` in the `Main` folder. Otherwise, the following 2 commands will not work.

### --analyze
Command: `python main.py --analyze`

Purpose: It will conduct Exploratory Data Analysis (EDA) on the properties off the database.

Expected output: 
* a summary table to the terminal.
* a variety of graphs (should be 6) that will appear in a seperate popup window (the next graph will not be shown unless you exit out of the window of the current graph).
* a heat geographic heat map (should appear as `heatmap.html`) of current prices that will be saved to the current directory (inside `Main`). You can open it in your browser to interact with it.

### --predict 
Command: `python main.py --predict`

Purpose: It will use a linear regression machine learning model create predicted prices of the properties off the database and compare it with the actual price to determine which properties are undervalued (ideal for investment). 

Expected output:
* a list of 5 properties with the best value. It will have their Zillow ID, actual price, predicted price, and the difference between the two. It will be shown in the terminal.
* a variety of graphs (should be 5) that will appear in a seperate popup window (the next graph will not be shown unless you exit out of the window of the current graph).
* a heat geographic heat map (should appear as `price_difference_heatmap.html`) that will be saved to the current directory (inside `Main`). You can open it in your browser to interact with it.

## --info
Command: `python main.py --info [zillow id]`

Purpose: It will request house data for the provided `zillow id` and save a formatted json file.

Expected output:
* there `will not` be an output for this command; however, there should be a json file, `data.json`, created within the `Main` folder.

## --addr
Command: `python main.py --info [Zillow ID] --addr`

Purpose: It will provide information about the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--addr` flag will provide the address of the property.

Expected output: 
* The street address and zip code of the property.

## --describe
Command: `python main.py --info [Zillow ID] --describe`

Purpose: It will provide a description of the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--describe` flag will provide the description of the property.

Expected output:
* The description of the property written by the broker.

## --school
Command: `python main.py --info [Zillow ID] --school`

Purpose: It will provide information about the schools near the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--school` flag will provide the information about the schools near the property.

Expected output:
* The name of the school, the type of school, the grade level, the distance from the property, and the rating of the school.

## --comp
Command: `python main.py --info [Zillow ID] --comp`

Purpose: It will provide information about the comparable properties near the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--comp` flag will provide the information about the comparable properties near the property.

Expected output:
* Links to the comparable properties near the property.

## --nearby
Command: `python main.py --info [Zillow ID] --nearby`

Purpose: It will provide a list of nearby cities with the given Zillow ID. The Zillow ID is a required argument for the command. The `--nearby` flag will provide the information about the nearby cities near the property.

Expected output:
* The name of the cities nearby the property.

## --hist
Command: `python main.py --info [Zillow ID] --hist`

Purpose: It will provide a list of historical prices of the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--hist` flag will provide the information about the historical prices of the property.

Expected output:
* The date and the price of the property.

## --year
Command: `python main.py --info [Zillow ID] --year`

Purpose: It will provide information about the year built of the property with the given Zillow ID. The Zillow ID is a required argument for the command. The `--year` flag will provide the information about the year built of the property.

Expected output:
* The year built of the property.

## Help
If the the last two commands do not work, or any other issue arises, please let us know.
