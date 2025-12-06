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