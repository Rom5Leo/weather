import streamlit as st
from weather.weather import get_weather_data
import pandas as pd


st.title("Weather App")

city_name = st.text_input("Enter the name of a city:")

if st.button("Get Weather"):
    if city_name:
        api_key = "792de6e244a5c651c61bba58e715aaf8"
        try:
            # Fetch weather data
            weather_data = get_weather_data(city_name, api_key)

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