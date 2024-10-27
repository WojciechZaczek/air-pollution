from datetime import timezone, datetime
import requests
from typing import Optional, List, Dict, Any
from weather_API_key import API_key
import URLs


class APIAirPollution:
    def __init__(self, city_name: str) -> None:
        """
        Initialize the APIAirPollution object with a specified city name.

        :param city_name: The name of the city for which data will be retrieved.
        """
        self.city_name = city_name

    @staticmethod
    def string_data_to_timestamp_unix(data: str) -> int:
        """
        Convert a date string in dd/mm/yyyy format to Unix timestamp (UTC).

        :param data: Date string in the format "dd/mm/yyyy".
        :return: Corresponding Unix timestamp as an integer.
        """
        return int(datetime.strptime(data, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())

    def get_coordinates(self) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve geographic coordinates of the city using the geolocation API.

        :return: List containing location data dictionaries or None if the city is not found.
        """
        coordinates_response = requests.get(f'{URLs.GEO_DIRECT_URL}q={self.city_name}&appid={API_key}')
        if coordinates_response:
            # print(f"City name: {coordinates_response.json()[0]['name']}")
            return coordinates_response.json()
        else:
            print("City not found or invalid city name.")
            return None

    def get_pollution(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve current air quality data for the city.

        :return: Dictionary containing air quality data or None if an error occurs.
        """
        lat = self.get_coordinates()[0]['lat']
        lon = self.get_coordinates()[0]['lon']
        pollution_response = requests.get(
            f'{URLs.AIR_POLLUTION_URL}lat={lat}&lon={lon}&appid={API_key}')
        if pollution_response:
            print(pollution_response.text)
            return pollution_response.json()
        else:
            print(pollution_response.text)
            return None

    def get_pollution_history(self, start_data: str, end_data: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve historical air quality data for the city between specified dates.

        :param start_data: Start date in the format "dd/mm/yyyy".
        :param end_data: End date in the format "dd/mm/yyyy".
        :return: Dictionary containing historical air quality data or None if an error occurs.
        """
        lat = self.get_coordinates()[0]['lat']
        lon = self.get_coordinates()[0]['lon']
        start_data_unix = self.string_data_to_timestamp_unix(start_data)
        end_data_unix = self.string_data_to_timestamp_unix(end_data)

        pollution_history_response = requests.get(
            f'{URLs.AIR_POLLUTION_HISTORY_URL}lat={lat}&lon={lon}&start={start_data_unix}&end={end_data_unix}&appid={API_key}')
        if pollution_history_response:
            print(pollution_history_response.text)
            return pollution_history_response.json()
        else:
            print(pollution_history_response.text)
            return None

    def get_weather_current(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve current weather data for the city.

        :return: Dictionary containing current weather data or None if an error occurs.
        """
        weather_response = requests.get(
            f'{URLs.WEATHER_CURRENT_URL}q={self.city_name}&appid={API_key}&units=metric')
        if weather_response:
            print(weather_response.text)
            return weather_response.json()
        else:
            print(weather_response.text)
            return None

    def get_weather_forecast_daily(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve daily weather forecast for the city for the next day.

        :return: Dictionary containing daily weather forecast or None if an error occurs.
        """
        lat = self.get_coordinates()[0]['lat']
        lon = self.get_coordinates()[0]['lon']
        forecast_response = requests.get(
            f'{URLs.WEATHER_DAILY_FORECAST_URL}lat={lat}&lon={lon}&cnt=1&appid={API_key}&units=metric')
        if forecast_response:
            print(forecast_response.text)
            return forecast_response.json()
        else:
            print(forecast_response.text)
            return None

# if __name__ == "__main__":
#     gdynia_api = APIAirPollution("Gdynia")
#     # gdynia_api.get_pollution()
#     # gdynia_api.get_pollution_history("01/01/2024", "03/01/2024")
#     # gdynia_api.get_weather_current()
#     gdynia_api.get_weather_forecast_daily()


