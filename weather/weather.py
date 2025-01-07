import requests
import unittest
from unittest.mock import patch

def get_weather_data(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.json().get('message')}")

    return response.json()

def display_weather_data(weather_data):
    if not weather_data:
        print("No weather data available.")
        return
    city = weather_data.get("name")
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    condition = weather_data["weather"][0]["description"]
    print(f"Weather in {city}:")
    print(f"  Temperature: {temp}°C")
    print(f"  Humidity: {humidity}%")
    print(f"  Condition: {condition.capitalize()}")

@patch("weather.weather.requests.get")
def test_get_weather_data_failure(self, mock_get):
    # Mocking a 404 response from the API
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"message": "city not found"}

    city_name = "InvalidCity"
    api_key = "dummy_api_key"

    # Asserting that an exception is raised for a 404 response
    with self.assertRaises(Exception) as context:
        get_weather_data(city_name, api_key)

    self.assertIn("API request failed", str(context.exception))
    self.assertIn("city not found", str(context.exception))