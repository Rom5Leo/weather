import streamlit as st
from weather.weather import get_weather_data, display_weather_data, display_date_time
import pandas as pd
import toml
from manage_settings import load_settings, save_settings
from streamlit_folium import folium_static
import folium

settings = load_settings()

st.title("Weather App")

# Show current settings
st.subheader("Current Settings")
st.write(f"Default Location: {settings['default_location'] or 'Not Set'}")
st.write(f"Temperature Unit: {'Celsius' if settings['temperature_unit'] == 'metric' else 'Fahrenheit'}")
st.write(f"Favorite Locations: {', '.join(settings['favorite_locations']) if settings['favorite_locations'] else 'None'}")

# Options to update settings
new_default_location = st.text_input("Enter a new default location:")


if st.button("Set Default Location"):

    if new_default_location:
        settings["default_location"] = new_default_location
        save_settings(settings)  # Save the updated settings
        st.success(f"Default location updated to {new_default_location}")
        if "rerun_flag" not in st.session_state:
            st.session_state["rerun_flag"] = False
        st.session_state["rerun_flag"] = not st.session_state["rerun_flag"]  # Trigger refresh
    else:
        st.warning("Please enter a valid city name.")

new_favorite = st.text_input("Enter a location to add to favorites:")
if st.button("Add to Favorite Locations"):

    if new_favorite:
        if new_favorite not in settings["favorite_locations"]:
            settings["favorite_locations"].append(new_favorite)
            save_settings(settings)  # Save the updated settings
            st.success(f"{new_favorite} added to favorites!")
            if "rerun_flag" not in st.session_state:
                st.session_state["rerun_flag"] = False
            st.session_state["rerun_flag"] = not st.session_state["rerun_flag"]  # Trigger refresh
        else:
            st.warning(f"{new_favorite} is already in favorites.")
    else:
        st.warning("Please enter a valid city name.")

if settings["favorite_locations"]:  # Check if there are favorites to remove
    city_to_remove = st.selectbox("Select a city to remove from favorites:", settings["favorite_locations"])
    if st.button("Remove from Favorites"):
        if city_to_remove in settings["favorite_locations"]:
            settings["favorite_locations"].remove(city_to_remove)
            save_settings(settings)
            st.success(f"{city_to_remove} removed from favorites!")
            if "rerun_flag" not in st.session_state:
                st.session_state["rerun_flag"] = False
            st.session_state["rerun_flag"] = not st.session_state["rerun_flag"]  # Trigger refresh
else:
    st.write("No favorite locations to remove.")

city_name = st.text_input("Enter the name of a city:")

if st.button("Get Weather"):
    if not city_name:
        city_name = settings["default_location"]
        if not city_name:
            st.warning("No default location set. Please enter a city name.")

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

            # Display weather icon
            icon_code = weather_data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            st.image(icon_url, caption="Current Weather Icon", use_container_width=100)

            # Show map of the location
            latitude = weather_data["coord"]["lat"]
            longitude = weather_data["coord"]["lon"]
            m = folium.Map(location=[latitude, longitude], zoom_start=10)
            folium.Marker(
                [latitude, longitude], popup=f"{city_name} ({latitude}, {longitude})"
            ).add_to(m)
            st.subheader("Map of the Location:")
            folium_static(m)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a city name.")
