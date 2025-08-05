import streamlit as st
import pandas as pd
import pickle
import datetime

# Load trained model
model = pickle.load(open("rain_XGB_model.pkl", "rb"))

# Title
st.title("Rain Prediction App")

# --- Input fields ---
st.subheader("Enter Weather Details")

date = st.date_input("Date", datetime.date.today())
min_temp = st.number_input("Min Temperature (°C)")
max_temp = st.number_input("Max Temperature (°C)")
humidity_9am = st.number_input("Humidity at 9am (%)")
humidity_3pm = st.number_input("Humidity at 3pm (%)")
pressure_9am = st.number_input("Pressure at 9am (hPa)")
pressure_3pm = st.number_input("Pressure at 3pm (hPa)")
wind_speed_9am = st.number_input("Wind Speed at 9am (km/h)")
wind_speed_3pm = st.number_input("Wind Speed at 3pm (km/h)")

rain_today = st.selectbox("Did it Rain Today?", ["Yes", "No"])
rain_today = 1 if rain_today == "Yes" else 0

# Location encoding (only these 4 locations used during training)
location = st.selectbox("Location", ["Chennai", "Kolkata", "Mumbai", "New Delhi"])

# Extract date components
date_day = date.day
date_month = date.month

# --- One-hot encode location ---
location_chennai = 1 if location == "Chennai" else 0
location_kolkata = 1 if location == "Kolkata" else 0
location_mumbai = 1 if location == "Mumbai" else 0
location_newdelhi = 1 if location == "New Delhi" else 0

# --- Create input sample in correct order ---
input_features = [[
    min_temp, max_temp, humidity_9am, humidity_3pm,
    pressure_9am, pressure_3pm, wind_speed_9am, wind_speed_3pm,
    rain_today,
    location_chennai, location_kolkata, location_mumbai, location_newdelhi,
    date_month, date_day
]]

# --- Predict button ---
'''if st.button("Predict"):
    prediction = model.predict(input_features)[0]
    if prediction == 1:
        st.success("🌧️ It will rain tomorrow.")
    else:
        st.info("☀️ No rain expected tomorrow.")'''

# Predict
if st.button("Predict"):
    prediction = model.predict(input_features)[0]
    prediction_proba = model.predict_proba(input_features)[0][1]  # Probability of rain

    st.markdown(f"### 🌧️ Rain Prediction: {'Rain' if prediction == 1 else 'No Rain'}")
    st.markdown(f"### 📊 Probability of Rain: **{prediction_proba * 100:.2f}%**")