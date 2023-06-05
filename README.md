# real-estate-price-analysis
Real Estate Price Prediction and Investment Analysis

## Client

Leo Dixon, Executive MBA PhD Candidate, Adjunct Faculty, Daniels College of Business, University of Denver, leo.dixon@du.edu
Description

## Description

This project aims to develop a potentially profitable investment opportunities in the housing market.
By leveraging historical and current data from the real estate market and a machine learning model, the
tool enables user to make informed decisions and navigate the market with confidence.

The project utilizes Python as the primary programming language and leverages the Scrapeak API to
scrape data from Zillow, a leading real estate marketplace. This ensures access to comprehensive and
up-to-date information for analysis and modeling.

The system architecture is designed with two keys objectives in mind:

1. `Data Acquisition and Analysis`: The system efficiently collects data from Zillow through the Scrapeak
API and stores it in a database. It provides robust analysis capabilities to gain insights into the real
estate market. This includes exploring data trends, patterns, and correlations that can influence 
property prices and investment opportunities.

2. `User-Focused Property Exploration`: The system offers users the flexibility to select specific 
properties they wish to explore further. It provides detailed and specific information about the selected
property, allowing users to make informed decisions based on their preferences and requirements.

This program does not necessitate the use of a particular development environment or anything like
that, so feel free to download the program and use it right away (after following the instructions 
below).

Below, in the `Getting the Program to Work` section, you will find a guide on how to set up your system for the program, how to get started with
the program, how to use it, the expected outputs, and visions for the future!

For technical look at the system architecture, please refer to the diagram below also found in the
`Diagrams` folder:

<img width="373" alt="software architecture diagram" src="https://github.com/dussec/real-estate-price-analysis/assets/95201389/eccf48b2-e3d0-46fb-8cf8-4843819fe4ed">

## Getting the Program to work

**`!NOTE`**: Please use `pip3` instead of `pip` in the following install instructions if you have the latest python release.

1. If you haven't already, install the latest version of Python. You can install it from here: [website](https://www.python.org/downloads/)
2. In a terminal window, run the following command lines to install the necessary dependencies for the program:
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

**`!NOTE`**: Please use `python3` instead of `python` in the following commands if you have the latest python release.

### --url 
Command: `python main.py --url "[Zillow search url]"`

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

Purpose: It will request house data for the provided `zillow id` and save two formatted `json` files.
One of the files, `hist.json`, contains the historical prices of the property. The other file, `data.json`, contains the data for all the other information about the property.

Expected output:
* there `will not` be an output for this command; however, there should be two json file, `data.json` & `hist.json`, created within the `Main` folder.

## --addr
Command: `python main.py --addr`

Purpose: It will provide information about the property with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--addr` flag will provide the address of the property.

Expected output: 
* The street address and zip code of the property.
    * Format: `123 Main St 12345`

## --describe
Command: `python main.py --describe`

Purpose: It will provide a description of the property with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--describe` flag will provide the description of the property.

Expected output:
* The description of the property written by the broker.
  * Format: `paragraph of text`

## --school
Command: `python main.py --school`

Purpose: It will provide information about the schools near the property with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--school` flag will provide the information about the schools near the property.

Expected output:
* The name of the school, the type of school, the grade level, the distance from the property, and the rating of the school.
    * Format: `school name, distance, school rating, grade level`

## --comp
Command: `python main.py --comp`

Purpose: It will provide information about the comparable properties near the property with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--comp` flag will provide the information about the comparable properties near the property.

Criteria for comparable properties:
1) Proximity to the property
2) Property type
3) Size and specifications
4) Time frame of sale or listing

Expected output:
* Links to the comparable properties near the property.
    * Format: `clickable links to the comparable properties`
      * `https://www.zillow.com/homedetails/123-Main-St-12345/12345678_zpid/`

## --nearby
Command: `python main.py --nearby`

Purpose: It will provide a list of nearby cities with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--nearby` flag will provide the information about the nearby cities near the property.

Expected output:
* The name of the cities nearby the property.
    * Format: `city Name`

## --hist
Command: `python main.py --hist`

Purpose: It will provide a list of historical prices of the property with the given Zillow ID. This command does not take arguments it uses the data stored in `hist.json`. The `--hist` flag will provide the information about the historical prices of the property.

Expected output:
* Date of transaction
* Price for transaction
* Price per squareFoot at the time of sale
* Price change rate in percentage
* Event type (Sold, Listed, etc.)

## --year
Command: `python main.py --year`

Purpose: It will provide information about the year built of the property with the given Zillow ID. This command does not take arguments it uses the data stored in `data.json`. The `--year` flag will provide the information about the year built of the property.

Expected output:
* The year built of the property.
    * Format: `year started - year completed`

## Making sense of the output from the `--analyze` and `--predict` commands

Below is a picture explaining the different graphs and outputs from the `--analyze` and `--predict` commands.
This can also be found in the `Diagrams` folder:

### --analyze:

![image](https://github.com/dussec/real-estate-price-analysis/assets/130081083/b1ed48f0-fa85-4102-bdb5-896c07139b1c)

### --predict:

![image](https://github.com/dussec/real-estate-price-analysis/assets/130081083/66921f71-dacb-490e-aa09-bcadd7cc536b)

## Future Work

In the future, there are several exciting avenues to explore and enhance this
project. Firstly, developing a Graphical User Interface (GUI) would provide a
user-friendly platform for easy interaction and visualization of data. 
Secondly, accessing the Zillow Developer API could offer access to richer data
, such as historical property information and market trends, enabling more 
accurate predictive models. Gathering additional data, such as crime rates 
and school district ratings, would further improve the models' accuracy and
provide more comprehensive suggestions. Expanding the range of graphs and
visualizations would enable deeper exploration and analysis of the gathered
data. Integrating financial data, including mortgage rates and economic 
indicators, would provide a holistic view of the real estate market. 
Lastly, expanding the database to include more property listings and 
historical data would facilitate long-term trend analysis. 
These future endeavors will transform this project into a powerful 
real estate analysis tool, empowering users with valuable insights and 
supporting informed investment decisions.

## Help

If you have any questions or need help with the project, 
please contact us at:

* [Robel Mamo](mailto:robel.mamo@du.du)
* [Ibraheem Qureshi](mailto:ibraheem.qureshi@du.edu)
* [Jordan Sutherland](mailto:jordan.sutherland@du.edu)
* [Karthik Turimella](mailto:karthik.turimella@du.edu)
