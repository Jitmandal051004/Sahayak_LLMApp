import os
import json
import shutil
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from enum import Enum
import time
from utility_function import get_lat_lon, get_soil_data, get_weather_data, save_to_jsonlines, retreive_data, format_prompt, prop_retreiver

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
        font-size: 1.5rem;
    }

    .result {
        font-family: "Playwrite IT Moderna", cursive;
        font-size: 1rem;
        color: #232b2b;
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

    /*answer*/
    .stAlert {
        background-color: #cce5ff; /* Light blue background */
        border-color: #b8daff; /* Border color */
        font-family: "Playwrite IT Moderna", cursive;
        font-size: 1.2rem;
        color: #232b2b;
    }

    .stAlert > div:first-child {
        border-radius: 8px; /* Rounded corners */
        padding: 12px; /* Padding around content */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Krishi Sahayak</h1>', unsafe_allow_html=True)

left_column, middlespace ,right_column = st.columns([2.1,1.5,1.4])
with left_column:
    location_name = st.text_input("Location")

lat, lon, weather = None, None, None
bulk_den, bdod_unit, nitrogen, n_unit, ph, ph_unit, soc, soc_unit, clay, clay_p, sand, sand_p, silt, silt_p = [None] * 14

if location_name:
    f_lat, f_lon = get_lat_lon(location_name, GEOCODE_API_KEY)
    lat = int(round(f_lat))
    lon = int(round(f_lon))
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
                weather = weather_data["weather"][0]["description"]
                st.markdown(f'<p class="result">Weather: {weather_data["weather"][0]["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Humidity: {weather_data["main"]["humidity"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Wind Speed: {weather_data["wind"]["speed"]} m/s</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Precipitation: {weather_data.get("rain", {}).get("1h", 0)} mm</p>', unsafe_allow_html=True)
                bulk_den, bdod_unit = prop_retreiver(soil_data=soil_data, x=0)
                st.markdown(f'<p class="result">Fine earth density: {bulk_den} {bdod_unit}</p>', unsafe_allow_html=True)
                nitrogen, n_unit = prop_retreiver(soil_data=soil_data, x=2)
                st.markdown(f'<p class="result">Total nitrogen g/kg: {nitrogen} {n_unit}</p>', unsafe_allow_html=True)
                ph, ph_unit = prop_retreiver(soil_data=soil_data, x=3)
                st.markdown(f'<p class="result">soil ph: {ph} pH</p>', unsafe_allow_html=True)
                soc, soc_unit = prop_retreiver(soil_data=soil_data, x=6)
                st.markdown(f'<p class="result">Soil organic carbon g/kg: {soc} {soc_unit}</p>', unsafe_allow_html=True)
                clay, clay_p = prop_retreiver(soil_data=soil_data, x=1)
                sand, sand_p = prop_retreiver(soil_data=soil_data, x=4)
                silt, silt_p = prop_retreiver(soil_data=soil_data, x=5)
                if clay or sand or silt:
                    st.markdown(f'<p class="result">Sand%: {sand} {sand_p}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="result">Clay%: {clay} {clay_p}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="result">silt%: {silt} {silt_p}</p>', unsafe_allow_html=True)
        else:
            st.error("Failed to retrieve soil or weather data.")
    else:
        st.error("Failed to retrieve latitude and longitude for the location.")

# Handle Discounts API request if data source is selected and a question is provided
with left_column:
    question = st.text_input("How Can I help You in Your farming ?")
    if location_name and lat and lon and soil_data and weather_data and question:
        processsed_data = retreive_data(question, location_name, bulk_den, nitrogen, ph, soc, clay, sand, silt)
        Prompt = format_prompt(processsed_data)
        print(Prompt)
        if question and Prompt:
            url = f'http://{api_host}:{api_port}/'
            data = {"query": Prompt}

            response = requests.post(url, json=data)
            print(response)
            if response.status_code == 200:
                st.write("### Answer")
                print(response.json())
                st.info(response.json())
            else:
                st.error(f"Failed to send data to Soil_data. Status code: {response.status_code}")
