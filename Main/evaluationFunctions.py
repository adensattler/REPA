from database import DatabaseManager
from datetime import datetime, timedelta
import requests
import json

# evaulation functions

# repair costs set to 0, can be changed
repairCosts = 0

# calculate expected rent, minimum rent should be 1% of purchase
# DB: monthly_rent
def onePercentRule(purchasePrice, repairCosts, loanValue):
    closingCosts = 0.06 * loanValue
    return (purchasePrice + closingCosts + repairCosts) * 0.1

# capitalization rate
# DB: cap_rate
def capRate(zpid, avgRent, avgAnnualCost, purchasePrice):
    cap = ((avgRent * 11.5 - avgAnnualCost) / purchasePrice) * 100
    database = DatabaseManager('zillow_listings.db')
    
    return cap

# break-even ratio 
# determines viability EXCLUDING initital costs like down payment
# DB: break_even
def breakEven(expenses, rentIncome):
    return (expenses / rentIncome) * 100

# mortgage monthly payments

# 30 year fixed
def thirtyFixed(purchasePrice, downPayment, interestRate):
    loan = purchasePrice - downPayment
    monthly = (loan * (interestRate / 12) * (1 + (interestRate / 12))**(12*30)) / ((1 + (interestRate / 12))**(12*30) - 1)
    return round(monthly, 2)

# 15 year fixed
def fifteenFixed(purchasePrice, downPayment, interestRate):
    loan = purchasePrice - downPayment
    monthly = (loan * (interestRate / 12) * (1 + (interestRate / 12))**(12*15)) / ((1 + (interestRate / 12))**(12*15) - 1)
    return round(monthly, 2)

# interest only 
# DB: interest_est
def interestOnly(purchasePrice, downPayment, interestRate):
    loan = purchasePrice - downPayment
    monthly = loan * (interestRate / 12) 
    return round(monthly, 2)

def PriceRelativeArea(zpid, purchasePrice, zipcode):
    database = DatabaseManager('zillow_listings.db')
    prices = database.get_area_prices(zipcode)
    total = 0
    for i in prices:
        total = total + i["price"]
    average = total / (len(prices))
    percentDif = round(((purchasePrice/average)-1) * 100, 2)
    database.update_property_db(zpid,"rel_price",percentDif)




