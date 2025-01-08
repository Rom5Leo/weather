import streamlit as st
from weather.weather import get_weather_data, display_weather_data, display_date_time
import pandas as pd
import toml


st.title("Weather App with Local Date and Time")

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

            local_time = display_date_time(weather_data["timezone"])  # Get the local time
            timezone_offset_hours = weather_data["timezone"] // 3600  # Convert seconds to hours
            timezone_formatted = f"UTC{'+' if timezone_offset_hours >= 0 else ''}{timezone_offset_hours}"  # Format as UTC±X

            # Display weather data in a table
            weather_df = pd.DataFrame({
                "Metric": ["Temperature (°C)", "Humidity (%)", "Condition", "Time Zone", "Local Time"],
                "Value": [
                weather_data["main"]["temp"],
                weather_data["main"]["humidity"],
                weather_data["weather"][0]["description"].capitalize(),
                timezone_formatted,
                local_time
                ]
            })
            st.table(weather_df)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a city name.")
