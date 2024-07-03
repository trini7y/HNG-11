from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests

app = Flask(_name_)


headers = {'Authorization': 'Bearer 0d9e78a4407977'}
API_KEY = "6ed1d1b943ab46b9804145041240207"
IP_API_KEY = 'b5ef005b5ede469f9e8bbff8a3031f3b'

def get_user_location():
    try:
        # response = requests.get('https://jsonip.com')
        # return response.json()
        response = requests.get(f'https://ipgeolocation.abstractapi.com/v1/?api_key={IP_API_KEY}&ip_address=')
        # print(response.status_code)
        # print(response.json())
        return response.json()
    except:
        print("Error: Unable to detect your location.")
        return None

@app.route('/api/hello/<name>', methods=['GET'])
def hello(name):
    visitor_name = name
    client_ip = get_user_location()
    # print("Client IP", client_ip, "Name", name)

    # Get temperature from weather API
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={client_ip['ip_address']}")
    weather_data = response.json()
    print("Weather Data",weather_data)
    temperature = weather_data['current']['temp_f']
    location = weather_data['location']['name']
    state =  weather_data['location']['region']
    country = weather_data ['location']['country']

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}, {state}, {country}'
    return jsonify({'client_ip': client_ip['ip_address'], 'location': location, 'greeting': greeting})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)