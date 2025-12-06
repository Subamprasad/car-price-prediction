<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle as pk

app = Flask(__name__)

model = pk.load(open('model.pkl', 'rb'))

cars_data = pd.read_csv('Cardetails.csv')

def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()

cars_data['name'] = cars_data['name'].apply(get_brand_name)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/dropdown-data', methods=['GET'])
def get_dropdown_data():
    return jsonify({
        'brands': sorted(cars_data['name'].unique().tolist()),
        'fuels': sorted(cars_data['fuel'].unique().tolist()),
        'seller_types': sorted(cars_data['seller_type'].unique().tolist()),
        'transmissions': sorted(cars_data['transmission'].unique().tolist()),
        'owners': sorted(cars_data['owner'].unique().tolist())
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        input_data = pd.DataFrame([[
            data['name'],
            data['year'],
            data['km_driven'],
            data['fuel'],
            data['seller_type'],
            data['transmission'],
            data['owner'],
            data['mileage'],
            data['engine'],
            data['max_power'],
            data['seats']
        ]], columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 
                     'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats'])
        
        input_data['owner'].replace(
            ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'],
            [1, 2, 3, 4, 5],
            inplace=True
        )
        
        input_data['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
        input_data['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
        input_data['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
        
        brands_map = {
            'Maruti': 1, 'Skoda': 2, 'Honda': 3, 'Hyundai': 4, 'Toyota': 5,
            'Ford': 6, 'Renault': 7, 'Mahindra': 8, 'Tata': 9, 'Chevrolet': 10,
            'Datsun': 11, 'Jeep': 12, 'Mercedes-Benz': 13, 'Mitsubishi': 14, 'Audi': 15,
            'Volkswagen': 16, 'BMW': 17, 'Nissan': 18, 'Lexus': 19, 'Jaguar': 20,
            'Land': 21, 'MG': 22, 'Volvo': 23, 'Daewoo': 24, 'Kia': 25,
            'Fiat': 26, 'Force': 27, 'Ambassador': 28, 'Ashok': 29, 'Isuzu': 30, 'Opel': 31
        }
        input_data['name'] = input_data['name'].map(brands_map)
        
        car_price = model.predict(input_data)[0]
        
        return jsonify({'price': float(car_price)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
=======
import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st

model = pk.load(open('model.pkl', 'rb'))

st.header('Car Price Prediction ML Model')

cars_data = pd.read_csv('Cardetails.csv')


def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()


cars_data['name'] = cars_data['name'].apply(get_brand_name)

name = st.selectbox('Select Car Brand', cars_data['name'].unique())
year = st.slider('Car Manufactured Year', 1994, 2024)
km_driven = st.slider('No of kms Driven', 11, 200000)
fuel = st.selectbox('Fuel type', cars_data['fuel'].unique())
seller_type = st.selectbox('Seller  type', cars_data['seller_type'].unique())
transmission = st.selectbox('Transmission type', cars_data['transmission'].unique())
owner = st.selectbox('Seller  type', cars_data['owner'].unique())
mileage = st.slider('Car Mileage', 10, 40)
engine = st.slider('Engine CC', 700, 5000)
max_power = st.slider('Max Power', 0, 200)
seats = st.slider('No of Seats', 5, 10)

if st.button("Predict"):
    input_data_model = pd.DataFrame(
        [[name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]],
        columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine',
                 'max_power', 'seats'])

    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
                                       'Fourth & Above Owner', 'Test Drive Car'],
                                      [1, 2, 3, 4, 5], inplace=True)
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
    input_data_model['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
                                      'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
                                      'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
                                      'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
                                      'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                      24, 25, 26, 27, 28, 29, 30, 31]
                                     , inplace=True)

    car_price = model.predict(input_data_model)

    st.markdown('Car Price is going to be = ' + str(car_price[0]))
>>>>>>> de01f217eaf657f1c2878e8acb5da60bf25724f0
