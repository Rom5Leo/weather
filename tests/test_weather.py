import unittest
from unittest.mock import patch
from weather.weather import get_weather_data

class TestWeather(unittest.TestCase):

    @patch("weather.weather.requests.get")
    def test_get_weather_data_success(self, mock_get):
        # Mocking a successful response
        mock_response = {
            "name": "London",
            "main": {"temp": 15, "humidity": 80},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        city_name = "London"
        api_key = "dummy_api_key"
        response = get_weather_data(city_name, api_key)

        self.assertEqual(response["name"], "London")
        self.assertEqual(response["main"]["temp"], 15)
        self.assertEqual(response["weather"][0]["description"], "clear sky")

    @patch("weather.weather.requests.get")
    def test_get_weather_data_failure(self, mock_get):
        # Mocking a 404 response
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"message": "city not found"}

        city_name = "InvalidCity"
        api_key = "dummy_api_key"

        with self.assertRaises(Exception) as context:
            get_weather_data(city_name, api_key)

        self.assertIn("API request failed", str(context.exception))
        self.assertIn("city not found", str(context.exception))

if __name__ == "__main__":
    unittest.main()


