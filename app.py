# import for stramlit app
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from utility_functions import get_lat_lon, get_soil_data, get_weather_data, save_to_jsonlines
# import for rag server
import logging
import pathway as pw
import yaml
from dotenv import load_dotenv

from pathway.udfs import DiskCache, ExponentialBackoffRetryStrategy
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from pathway.xpacks.llm.vector_store import VectorStoreServer

load_dotenv()
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
    Prompt = st.text_input("How Can I help You in Your farming ?")

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
            save_to_jsonlines(data, filename="./build/jsonline/soil_data.jsonl")
            with right_column:
                st.markdown('<h3 class="results-title">Results:</h3>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Temperature: {weather_data["main"]["temp"]}°C</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Weather: {weather_data["weather"][0]["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Humidity: {weather_data["main"]["humidity"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Wind Speed: {weather_data["wind"]["speed"]} m/s</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Precipitation: {weather_data.get("rain", {}).get("1h", 0)} mm</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Soil Type: {soil_data["properties"]["layers"][1]["name"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Soil pH: {soil_data["properties"]["layers"][3]["unit_measure"]["d_factor"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result">Nitrogen Content: {soil_data["properties"]["layers"][2]["unit_measure"]["d_factor"]} {soil_data["properties"]["layers"][2]["unit_measure"]["mapped_units"]}</p>', unsafe_allow_html=True)
        else:
            st.error("Failed to retrieve soil or weather data.")
    else:
        st.error("Failed to retrieve latitude and longitude for the location.")