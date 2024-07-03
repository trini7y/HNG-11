from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests
import json

app = Flask(__name__)


def getUserLocation():
    try:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        return ip
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
    return json.dumps({'client_ip': ip, 'location': location, 'greeting': greeting}, sort_keys=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)