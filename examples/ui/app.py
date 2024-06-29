import os
import json
import shutil
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from enum import Enum
import time
from utility_function import get_lat_lon, get_soil_data, get_weather_data, save_to_jsonlines

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = int(os.environ.get("PORT", 8080))
GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

st.set_page_config(layout="wide")

css = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
    }}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playwrite+IT+Moderna:wght@300&family=Playwrite+MX&family=Roboto:wght@400;500&display=swap');    
    .title {
        font-family: "Playwrite MX", cursive;
        font-size: 3em;  /* Significantly increases the font size */
        font-weight: bold;  /* Makes the font bold */
        color: #ffffff;  /* Changes the text color to white */
        text-shadow: 3px 3px 8px black;  /* Enhances the text shadow for better visibility */
        padding: 15px 20px;  /* Adds more padding around the text */
        margin-bottom: 1.2rem;
    }

    .results-title {
        font-family: "Playwrite MX", cursive;
        font-size: 1.8rem;
    }

    .result {
        font-family: "Playwrite IT Moderna", cursive;
        font-size: 1.2rem;
        color: #FFFFFF;
        margin: 0px 0px 2px;
        text-shadow: 3px 3px 8px black;
    }
    
    /*label css*/
    .st-emotion-cache-qgowjl {
        font-family: "Playwrite IT Moderna", cursive;
        color: #FFFFFF;  /* Label color */
    }
            
    .st-emotion-cache-qgowjl p {
        font-size: 1.2rem;
        margin-bottom: 5px;
    }
            
    /*text-input*/
    .st-ax {
    font-family: "Roboto", sans-serif;
    font-weight: 400;
    }
    .st-ah {
    width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Krishi Sahayak</h1>', unsafe_allow_html=True)

left_column, middlespace ,right_column = st.columns([2.1,1.5,1.4])
with left_column:
    location_name = st.text_input("Location")

if location_name:
    lat, lon = get_lat_lon(location_name, GEOCODE_API_KEY)
    if lat and lon:
        soil_data = get_soil_data(lat, lon)
        weather_data = get_weather_data(lat, lon, WEATHER_API_KEY)
        if soil_data and weather_data:
            data = {
                "location": location_name,
                "latitude": lat,
                "longitude": lon,
                "soil_data": soil_data,
                "weather_data": weather_data
            }
            save_to_jsonlines(data, filename="../data/soil_data.jsonl")
            with right_column:
                st.markdown('<h3 class="results-title">Results:</h3>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Temperature: {weather_data["main"]["temp"]}°C</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Weather: {weather_data["weather"][0]["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Humidity: {weather_data["main"]["humidity"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Wind Speed: {weather_data["wind"]["speed"]} m/s</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Precipitation: {weather_data.get("rain", {}).get("1h", 0)} mm</p>', unsafe_allow_html=True)
                # st.markdown(f'<p class="result">Soil Type: {soil_data["properties"]["layers"][1]["name"]}</p>', unsafe_allow_html=True)
                # st.markdown(f'<p class="result">Soil pH: {soil_data["properties"]["layers"][3]["unit_measure"]["d_factor"]}</p>', unsafe_allow_html=True)
                # st.markdown(f'<p class="result">Nitrogen Content: {soil_data["properties"]["layers"][2]["unit_measure"]["d_factor"]} {soil_data["properties"]["layers"][2]["unit_measure"]["mapped_units"]}</p>', unsafe_allow_html=True)
        else:
            st.error("Failed to retrieve soil or weather data.")
    else:
        st.error("Failed to retrieve latitude and longitude for the location.")

# Handle Discounts API request if data source is selected and a question is provided
with left_column:
    Prompt = st.text_input("How Can I help You in Your farming ?")
    url = f'http://{api_host}:{api_port}/'
    data = {"query": Prompt}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Soil_data. Status code: {response.status_code}")