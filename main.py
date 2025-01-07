from weather.weather import get_weather_data, display_weather_data

if __name__ == "__main__":
    API_KEY = "792de6e244a5c651c61bba58e715aaf8"
    city_name = input("Enter city name: ")
    try:
        weather_data = get_weather_data(city_name, API_KEY)
        display_weather_data(weather_data)
    except Exception as e:
        print(f"Error: {e}")

