import streamlit as st
from weather.weather import get_weather_data, display_date_time
import pandas as pd
import toml
from manage_settings import load_settings, save_settings
from streamlit_folium import folium_static
import folium

# Load settings
settings = load_settings()

# App title
st.title("🌦️ Weather App")

# Sidebar for user settings
st.sidebar.header("User Settings")
st.sidebar.subheader("Current Settings")
st.sidebar.write(f"**Default Location:** {settings['default_location'] or 'Not Set'}")
st.sidebar.write(f"**Temperature Unit:** {'Celsius' if settings['temperature_unit'] == 'metric' else 'Fahrenheit'}")
st.sidebar.write(
    f"**Favorite Locations:** {', '.join(settings['favorite_locations']) if settings['favorite_locations'] else 'None'}")

# Update default location
new_default_location = st.sidebar.text_input("Set a New Default Location:")
if st.sidebar.button("Set Default Location"):
    if new_default_location:
        settings["default_location"] = new_default_location
        save_settings(settings)
        st.sidebar.success(f"Default location updated to {new_default_location}")
        st.experimental_rerun()
    else:
        st.sidebar.warning("Please enter a valid city name.")

# Add favorite location
new_favorite = st.sidebar.text_input("Add to Favorite Locations:")
if st.sidebar.button("Add Favorite"):
    if new_favorite:
        if new_favorite not in settings["favorite_locations"]:
            settings["favorite_locations"].append(new_favorite)
            save_settings(settings)
            st.sidebar.success(f"{new_favorite} added to favorites!")
            st.experimental_rerun()
        else:
            st.sidebar.warning(f"{new_favorite} is already in favorites.")
    else:
        st.sidebar.warning("Please enter a valid city name.")

# Remove favorite location
if settings["favorite_locations"]:
    city_to_remove = st.sidebar.selectbox("Remove a Favorite Location:", settings["favorite_locations"])
    if st.sidebar.button("Remove Favorite"):
        settings["favorite_locations"].remove(city_to_remove)
        save_settings(settings)
        st.sidebar.success(f"{city_to_remove} removed from favorites!")
        st.experimental_rerun()
else:
    st.sidebar.write("No favorite locations to remove.")

# Main content area
st.subheader("🌍 Weather Information")
city_name = st.text_input("Enter the name of a city (leave blank to use default location):")

if st.button("Get Weather"):
    if not city_name:
        city_name = settings["default_location"]
        if not city_name:
            st.warning("No default location set. Please enter a city name.")

    if city_name:
        try:
            # Get API Key
            try:
                API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
            except Exception:
                local_secrets = toml.load(".streamlit/secrets.toml")
                API_KEY = local_secrets["OPENWEATHERMAP_API_KEY"]

            # Fetch weather data
            weather_data = get_weather_data(city_name, API_KEY)

            # Display weather data
            st.markdown(f"### Weather in {weather_data['name']}")
            st.write(f"**Temperature:** {weather_data['main']['temp']} °C")
            st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
            st.write(f"**Condition:** {weather_data['weather'][0]['description'].capitalize()}")

            # Local date and time
            local_time = display_date_time(weather_data["timezone"])
            st.write(f"**Local Time:** {local_time}")

            # Column layout for weather icon and details
            col1, col2 = st.columns([1, 2])
            with col1:
                icon_code = weather_data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, caption="Current Weather Icon", width=100)
            with col2:
                timezone_offset_hours = weather_data["timezone"] // 3600
                timezone_formatted = f"UTC{'+' if timezone_offset_hours >= 0 else ''}{timezone_offset_hours}"
                # weather_df = pd.DataFrame({
                #     "Metric": ["Temperature (°C)", "Humidity (%)", "Condition", "Time Zone", "Local Time"],
                #     "Value": [
                #         weather_data["main"]["temp"],
                #         weather_data["main"]["humidity"],
                #         weather_data["weather"][0]["description"].capitalize(),
                #         timezone_formatted,
                #         local_time
                #     ]
                # })
                # st.table(weather_df)
                # Prepare the data as a simple 2-column table
                weather_details = [
                    ("**Temperature (°C):**", f"{weather_data['main']['temp']} °C"),
                    ("**Humidity (%):**", f"{weather_data['main']['humidity']}%"),
                    ("**Condition:**", weather_data["weather"][0]["description"].capitalize()),
                    ("**Time Zone:**", timezone_formatted),
                    ("**Local Time:**", local_time),
                ]

                # Display weather details with Markdown
                st.markdown("### Weather Details")
                for metric, value in weather_details:
                    st.markdown(f"{metric} {value}")

            # Map
            latitude = weather_data["coord"]["lat"]
            longitude = weather_data["coord"]["lon"]
            st.markdown("### Map of the Location")
            m = folium.Map(location=[latitude, longitude], zoom_start=10)
            folium.Marker(
                [latitude, longitude],
                popup=f"{city_name} ({latitude}, {longitude})"
            ).add_to(m)
            folium_static(m)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a city name.")
