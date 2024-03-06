from database import DatabaseManager

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
def capRate(avgRent, avgAnnualCost, purchasePrice):
    return ((avgRent * 11.5 - avgAnnualCost) / purchasePrice) * 100

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
def interestOnly(purchasePrice, downPayment, interestRate):
    loan = purchasePrice - downPayment
    monthly = loan * (interestRate / 12) 
    return round(monthly, 2)




