import streamlit as st
from weather.weather import get_weather_data
import pandas as pd
import toml


st.title("Weather App")

city_name = st.text_input("Enter the name of a city:")

if st.button("Get Weather"):
    if city_name:
        # Use Streamlit's st.secrets if deployed; otherwise, load the local secrets file
        try:
            API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
        except Exception:
            local_secrets = toml.load(".streamlit/secrets.toml")
            API_KEY = local_secrets["OPENWEATHERMAP_API_KEY"]

#         st.write(f"API Key: {API_KEY}")  # For testing purposes only; remove this in production
        try:
            # Fetch weather data
            weather_data = get_weather_data(city_name, API_KEY)

            # Display weather information
            st.subheader(f"Weather in {weather_data['name']}:")
            st.write(f"Temperature: {weather_data['main']['temp']} °C")
            st.write(f"Humidity: {weather_data['main']['humidity']}%")
            st.write(f"Condition: {weather_data['weather'][0]['description'].capitalize()}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a city name.")

    if city_name:
        weather_df = pd.DataFrame({
            "Metric": ["Temperature (°C)", "Humidity (%)", "Condition"],
            "Value": [weather_data["main"]["temp"], weather_data["main"]["humidity"], weather_data["weather"][0]["description"].capitalize()]
        })
        st.table(weather_df)