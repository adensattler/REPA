# real-estate-price-analysis
Real Estate Price Prediction and Investment Analysis

## Client

Leo Dixon, Executive MBA PhD Candidate, Adjunct Faculty, Daniels College of Business, University of Denver, leo.dixon@du.edu
Description

## Description

The aim of this project is to develop a machine learning model that predicts real estate prices and identifies potentially profitable investment opportunities in the housing market using historical and current data of the real estate market.

Data Source: The real estate data can be obtained from sources like the Zillow API, or a public dataset like the U.S. Housing dataset available on Kaggle: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data



1. Collects data using Zillow api and web scraper to allow for individual houses real estate data and local historical data. Stored in a Sqlite server.

2. The collection of the data has built in cleaning with it to handle null and missing values

3. Use data collected to allow for the making of a dataframe object that allows for the creation of charts and graphs through mathplotlib

4. Use Sqlite server to train linear regression model for each individual state to come up with predicted values for houses.
