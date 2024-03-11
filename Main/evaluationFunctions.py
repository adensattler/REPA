from database import DatabaseManager

# evaulation functions

# repair costs set to 0, can be changed
repairCosts = 0

# calculate expected rent, minimum rent should be 1% of purchase
def onePercentRule(purchasePrice, repairCosts, downPayment, zestimateRent):
    loanValue = purchasePrice - downPayment
    closingCosts = 0.06 * loanValue
    expectedRent = (purchasePrice + closingCosts + repairCosts) * 0.1
    return expectedRent
        


# capitalization rate should be 5-10%, under 5% is lower risk but takes longer to recoup investment
# higher means more risk
# need to grab average rent of area, maybe zip code
def capRate(purchasePrice, loanValue, monthlyPayment, homeValue, zestimateRent, propertyTax):

    return ((zestimateRent * 12) - ((monthlyPayment * 12) + propertyTax) / homeValue)

x = capRate()
# break-even ratio 
# determines viability EXCLUDING initital costs like down payment - under 85% is optimal
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

# adjustable rate 