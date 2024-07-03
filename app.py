from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)


API_KEY = "6ed1d1b943ab46b9804145041240207"
IP_KEY = '23e70ad74b374925ac6e18e363d68a08'

def getUserLocation():
    try:
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr
        return user_ip
    except:
        print("Error: Unable to detect your location.")
        return None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    clientIp = getUserLocation()
    ip = clientIp
    if(ip):
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={ip}")
    else:
        response = "No Response"
    weatherData = response.json()
    temperature = weatherData['current']['temp_f']
    location = weatherData['location']['name']

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}'
    return jsonify({'client_ip': ip, 'location': location, 'greeting': greeting})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)