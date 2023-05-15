import pickle
import pandas as pd

# load the saved model from a file
with open('real_estate_model.pickle', 'rb') as f:
    model = pickle.load(f)

# make predictions using the loaded model

def make_prediction(zip_code, num_bedrooms, num_bathrooms, area, tax_ass_val): # parameters need to be updated when we decide on factors we want to include

    house_data = pd.DataFrame({
        'zip_code': zip_code,
        'num_bedrooms': num_bedrooms,
        'num_bathrooms': num_bathrooms,
        'area': area,
        'tax_ass_val': tax_ass_val
    })

    return model.predict(house_data)
