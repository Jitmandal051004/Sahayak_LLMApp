import requests
import json
import os

def get_lat_lon(location_name, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location_name}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            return lat, lon
    return None, None

def get_soil_data(lat, lon):
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property=bdod&property=clay&property=nitrogen&property=phh2o&property=sand&property=silt&property=soc&depth=0-30cm&depth=30-60cm&value=mean"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# def location_exist_in_file(location_name, filename = "soil_data.jsonl"):
#     if not os.path.exists(filename):
#         return False
#     with open(filename, 'r') as f:
#         for line in f:
#             existing_data = json.loads(line)
#             if existing_data.get("location_name") == location_name:
#                 return True
#     return False

def save_to_jsonlines(data, filename="soil_data.jsonl"):
    # if not location_exist_in_file(data["location_name"], './jsonline/soil_data.jsonl'):
    with open(filename, 'w') as f:
        json_line = json.dumps(data) + "\n"
        f.write(json_line)
    return True
    