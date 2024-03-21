# real-estate-price-analysis
Real Estate Price Prediction and Investment Analysis

## Client

Leo Dixon, Executive MBA PhD Candidate, Adjunct Faculty, Daniels College of Business, University of Denver, leo.dixon@du.edu

## Description

This project aims to help users find potentially profitable investment opportunities or "good deals" in the housing market.

By leveraging large amounts of data from the real estate market, a machine learning model, an AI Assistant, and numerous evaluation metrics, this tool enables user to make more informed decisions and navigate the market with confidence. 


Here's a brief overview of the tools and technologies used in the project:

### Technologies:
**Python**: Our project is primarily built using Python, a versatile and powerful programming language.

**Flask**: We rely on Flask, a Python-based web framework, for building our web application and managing server-side logic.

**HTML/CSS/JS**: For the frontend user interface design, we utilize a combination of HTML, CSS, and JavaScript to create an engaging and intuitive experience. We used the frontend framework [Bootstrap](https://getbootstrap.com/) for most of our UI design.

### APIs:   
**Scrapeak API**: Scrapes data from Zillow, allowing us to access comprehensive and up-to-date property information effortlessly.

**Google Places API**: To enhance user experience, we integrated the Google Places API for address search autocompletion.

**OpenAI Assistants API**: Allows us to create and interact with an AI Real Estate Assistant. This assistant adds an intelligent layer to our application, assisting users with various real estate-related inquiries and tasks.

### Other Tools:
**SQLite3**: We utilize SQLite3, a lightweight and self-contained SQL database engine, for managing our databases. SQLite3 offers simplicity and efficiency, making it an ideal choice for our application's data storage needs.

**scikit-learn (ML Linear Regression)**: Utilized to implement a linear regression model for property price prediction. This model enhances our application by providing users with estimated property prices based on relevant features.


The system architecture is designed with two keys objectives in mind:

1. `Data Acquisition and Analysis`: The system efficiently collects data from Zillow through the Scrapeak
API and stores it in a database. It provides robust analysis capabilities to gain insights into the real
estate market. This includes exploring data trends, patterns, and correlations that can influence 
property prices and investment opportunities.

2. `User-Focused Property Exploration`: The system offers users the flexibility to select specific 
properties they wish to explore further. It provides detailed and specific information about the selected
property, allowing users to make informed decisions based on their preferences and requirements.

The `Running the Program` section found below will walk you through setting up the program and how to get it to run on your system.

The [Routes & Functionality](#routes-&-functionality) section will describe how to use each part of the app and how they function. 

For technical look at the system architecture, please refer to the diagram below also found in the
`Diagrams` folder:

<img width="373" alt="software architecture diagram" src="https://github.com/dussec/real-estate-price-analysis/assets/95201389/eccf48b2-e3d0-46fb-8cf8-4843819fe4ed">

## Running the Program

1. Clone the repository onto your local machine. Choose a directory that you plan to have the program in, open a terminal window on that directory, and run the following command line to clone:
`git clone https://github.com/dussec/real-estate-price-analysis.git`

2. If you haven't already, install the latest version of Python. You can install it from here: [website](https://www.python.org/downloads/)

3. In a terminal window, run the following command to install the necessary dependencies for the program:
`pip install -r requirements.txt`

    **`!NOTE`**: Please use `pip3` instead of `pip` in the following install instructions if you have the latest python release.

4. Navigate to the `Main` directory and create a file called config.py. Add the following line with your Scrapeak API key to the file.
    `API_KEY = "YOUR_SCRAPEAK_API_KEY_HERE"`

5. Set your OpenAI API key using the instructions found [here](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key?context=python#:~:text=Set%20up%20your%20API%20key%20for%20all%20projects%20(recommended)) to enable the assistant functionality.

6. Change direectory or open a new terminal window on the folder `Main`. 

7. Run the Flask app by entering the command `flask run`, `python3 app.py`, or just hit the run button in your IDE. Open a browser and go to http://127.0.0.1:5000 to view the app.

## Routes & Functionality 
### Property Search
**Usage:** Enter the address or ZPID of a property you want to search for. If you don't have a property in mind you can always find one on [Zillow](https://www.zillow.com/). Searching a property will load a dedicated page for that property. The page also displays a list of recently searched properties and any properies you have favorited.

Details: Search history and favorites are drawn from the propertyDetails and favoriteList tables of the database respectively. Address search autocompletion functionality is powered by the Google Places API.

### Property Page(s)
Usage: Allows users to view numerous details and metrics related to a property that can help eveluate whether a property might be a good deal. Also allows users to interact with an AI assistant that has access to the data on that property and can answer almost any questions users may have!

### AI Assistant
The AI Assistant serves as a virtual real estate professional, providing assistance on property.html pages. It accesses data for a specific property stored in the `raw_json` attribute of the `propertyDetails` table in the database.

#### Files Related to the Assistant:

- **assistant.py**: This file contains all information related to the creation and usage of the AI Assistant. Refer to the file's comments for more details.
- **assistants/del-assistants.py**: A script designed to delete all assistant objects associated with your OpenAI account/key.
- **static/js/assistant.js**: Contains the frontend js code for interacting with the assistant on the `property.html` page.


### Listings Search
**Usage:** 
Go to the Zillow [website](https://www.zillow.com/) and search for homes (for sale) in the Denver. Try to include a variety of areas (Aurora, Centennial, etc) and filter the results to your liking. Once you're done with the search, copy the url from the address bar. Paste the URL into the search bar on the `Listings Search` page and hit submit.

Once you have submitted your search area, you can hit the predict or analyze buttons to process the mass of property data.

**Search:** Populates the listings table of the database with the data for every property in the requested search area.

**Predict:** Uses a linear regression machine learning model to predict prices of the properties in the database and compare them with the actual price to determine which properties are undervalued (ideal for investment). Outputs a list of the top five prospects to the user. **NOTE:** the original CLI version of the app created five additional [graphs](https://github.com/dussec/real-estate-price-analysis/assets/130081083/66921f71-dacb-490e-aa09-bcadd7cc536b) that are absent from the current version. See predict.py for more details.

**Analyze:** Conducts Exploratory Data Analysis (EDA) on the properties in the listings table of the database. Outputs a table to the webpage containing basic statistics on the sample of properties. **NOTE:** the original command line version of the application created seven additional [graphs](https://github.com/dussec/real-estate-price-analysis/assets/130081083/b1ed48f0-fa85-4102-bdb5-896c07139b1c) to visualize the data that are absent from the current version. See analyze.py for more details.

## Versions

### v0.0.0 
This is the original CLI version of the app developed by the original team of software developers in Spring 2023. It has been archived on the branch spring_cli_2023 for future reference and easy access.

### v1.0.0
This version implements the functionality of the original CLI version of the REPA software in a locally hosted Flask web app. It serves primarily as a GUI before reorganizing the system architecture and expand the functionality of the project to meet our client's vision.

### v1.0.1 (Sprint 1)
Represents the state of the software after the first development spring. Includes updates to the UI, overhaul of the system architecture, database management, search functionality, and stability of the app.

### v1.0.2 (Sprint 2)
This is the version completed of the web app after the second sprint. Updates include fully implemented AI real estate assistant, a UI overhaul, expansion of data/metrics displayed on the property page among other small features.

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

Property Analysis Algorithm
How are we going to decide if a house is a good deal?!
The factors that go into making that decision should be modifiable to fit user needs


## Help

If you have any questions or need help with the project, 
please contact us at:

* [Robel Mamo](mailto:robel.mamo@du.du)
* [Ibraheem Qureshi](mailto:ibraheem.qureshi@du.edu)
* [Jordan Sutherland](mailto:jordan.sutherland@du.edu)
* [Karthik Turimella](mailto:karthik.turimella@du.edu)
* 

