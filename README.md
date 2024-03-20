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

The `Functionality` section will describe how to use each part of the app and how they function. 

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

4. Go to the Zillow [website](https://www.zillow.com/) and search for homes (for sale) in the Denver. Try to include a variety of areas (Aurora, Centennial, etc) and a broad criteron for a large dataset. Once you're done with the search, copy the link in the address bar. If you wish, you can use this link already provided in the `zillow_example.txt` file under the 'Examples' folder.

## Routes & Functionality 
### Property Search
TODO:

### Property Details Page
TODO:

### AI Assistant
The AI Assistant serves as a virtual real estate professional, providing assistance on property pages. It accesses specific property data stored in the `propertyDetails` table of the database, accessible through the `raw_json` tab.

#### Files Related to the Assistant:

- **assistant.py**: This file contains all information related to the creation and usage of the AI Assistant. Refer to the file's comments for detailed instructions.
- **assistants/del-assistants.py**: A script designed to delete all assistant objects associated with your OpenAI account/key.
- **static/js/assistant.js**: This file contains the frontend code for interacting with the assistant on the `property.html` page.


### Listings Search
Usage:
The listings search is composed of three elements: a url search, a predict button, and an analyze button.

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
* 

