import streamlit as st
import pandas as pd
from enum import Enum
from dotenv import load_dotenv
import shutil
import datetime
import requests
import json
import io
import os

load_dotenv()

st.set_page_config(layout="wide")

css = f"""
    <style>
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
    }}
    #response{{
        background-color: black;
        padding: 10px;
        border-radius: 10px;
        font-size: 1rem;
        color: grey;
    }}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

left_column, right_column = st.columns([3,1])

with left_column:
    st.title("Krishi Sahayak")
    Prompt = st.text_input("How Can I help You in Your farming ?")



with right_column:
    location_name = st.text_input("")   
    # st.markdown('<div id="response">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="font-size: 1.8rem; color: grey;">Results:</h3>', unsafe_allow_html=True)
    st.write(f"Temperature: None")
    st.write(f"Soil Moisture: None")
    st.write(f"Humidity: None")
    # st.markdown('</div>', unsafe_allow_html=True)
