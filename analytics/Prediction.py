import pickle
import pandas as pd

model = None

def set_model(city):
    global model
    with open(f'{city}_Pred_Model.pickle', 'rb') as f:
        model = pickle.load(f)

# make predictions using the loaded model

def make_prediction(num_beds, num_baths, area, tax_ass_val, latitude, longitude): # parameters need to be updated when we decide on factors we want to include
    global model

    house_data = pd.DataFrame({
        'num_beds': [num_beds],
        'num_baths': [num_baths],
        'area': [area],
        'tax_ass_val': [tax_ass_val],
        'latitude': [latitude],
        'longitude': [longitude]
    })

    return model.predict(house_data)

def main():
    set_model('CO')
    print(make_prediction(2, 3, 1128, 221800, 39.782330, -104.962100))

if __name__ == '__main__':
    main()

'''
# make prediction using loaded model
new_data = pd.DataFrame({
    'num_beds': [2],
    'num_baths': [3],
    'area': [1128],
    'tax_ass_val': [221800],
    'latitude': [39.782330],
    'longitude': [-104.962100]
})
'''