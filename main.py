from weather.weather import get_weather_data, display_weather_data, display_date_time
import streamlit as st

if __name__ == "__main__":

    # Access the API key from Streamlit's secrets
    API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
    city_name = input("Enter city name: ")

    try:
        weather_data = get_weather_data(city_name, API_KEY)

        display_weather_data(weather_data)

        timezone_offset = weather_data["timezone"]  # Get the timezone offset from the weather data
        local_time = display_date_time(timezone_offset)
        print(f"Local Date and Time in {city_name}: {local_time}")

    except Exception as e:
        print(f"Error: {e}")

