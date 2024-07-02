import requests
import json
from tenacity import retry, wait_exponential, stop_after_attempt, RetryError

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

def save_to_jsonlines(data, filename="soil_data.jsonl"):
    # if not location_exist_in_file(data["location_name"], './jsonline/soil_data.jsonl'):
    with open(filename, 'w') as f:
        json_line = json.dumps(data) + "\n"
        f.write(json_line)
    return True

def prop_retreiver(soil_data,x):
    if soil_data["properties"]["layers"][x]["depths"][0]["values"]["mean"] and soil_data["properties"]["layers"][x]["unit_measure"]["d_factor"]:
        value = soil_data["properties"]["layers"][x]["depths"][0]["values"]["mean"] / soil_data["properties"]["layers"][x]["unit_measure"]["d_factor"]
        if not 3:
            unit = soil_data["properties"]["layers"][x]["unit_measure"]["target_units"]
        else: 
            unit = soil_data["properties"]["layers"][x]["unit_measure"]["mapped_units"]
    else:
        value = None
        unit = None

    return value, unit

def retreive_data(question, location_name, bulk_den, nitrogen, ph, soc, clay, sand, silt):
    data = {
        "question": question,
        "Approx_location_name": location_name,
        "Bulk density of the fine earth fraction (kilograms per cubic decimeter)": bulk_den,
        "Total nitrogen (N) g/kg": nitrogen,
        "ph of soil": ph,
        "Soil organic carbon g/kg": soc,
        "clay percentage": clay,
        "sand percentage": sand,
        "silt percentage": silt,
    }

    clean_data = {key: str(value).strip() for key, value in data.items()}

    return clean_data

def format_prompt(data):
    if data is None:
        return "Invalid data provided."

    # Extracting the elements from the dictionary
    question = data.get("question", "")
    location_name = data.get("Approx_location_name", "")
    bulk_den = data.get("Bulk density of the fine earth fraction (kilograms per cubic decimeter)", "")
    nitrogen = data.get("Total nitrogen (N) g/kg", "")
    ph = data.get("ph of soil", "")
    soc = data.get("Soil organic carbon g/kg", "")
    clay = data.get("clay percentage", "")
    sand = data.get("sand percentage", "")
    silt = data.get("silt percentage", "")

    # Create the formatted prompt
    prompt = f"Question: {question}\nLocation: {location_name}\nBulk Density: {bulk_den}kilograms per cubic decimeter\nTotal Nitrogen: {nitrogen} g/kg\npH of Soil: {ph}\nSoil Organic Carbon: {soc} g/kg\nClay Percentage: {clay}%\nSand Percentage: {sand}%\nSilt Percentage: {silt}%"
    return prompt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def fetch_data_from_server(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Server is not ready yet.")
    return response.json()