import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(Path(__file__).resolve().parent.parent))

from abstract_strategy import ExtractStrategy
import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException
from weather_API_key import API_key
from gcloud.utils import URLs
from gcloud.utils.static import string_data_to_timestamp_unix, load_config
# from dotenv import load_dotenv
#
# dotenv_path = Path('../../../.env')
# load_dotenv(dotenv_path)


class OpenweatherDataExtractor(ExtractStrategy):
    """
       Extractor class for retrieving data using the OpenWeather API and Air Pollution API.
       """

    def __init__(self) -> None:
        """
        Initialize the OpenWeatherDataExtractor with a persistent HTTP session
        and city configuration loaded from a YAML file.
        """
        # self.config_path =  Path(__file__).resolve().parent.parent / "utils" / "config" / "cities_config.yaml"
        self.config_path =  "utils\\config\\cities_config.yaml"
        self.cities = load_config(self.config_path)
        self.session = requests.Session()

    def get_pollution(self, city: dict) -> Optional[Dict[str, Any]]:
        """
        Retrieve current air quality data for the specified city.

        :param city: Dictionary containing city data with keys "name", "lat", "lon".
        :return: Dictionary containing air pollution data or None if an error occurs.
        """
        lat, lon = city['lat'], city['lon']

        try:
            response = self.session.get(f'{URLs.AIR_POLLUTION_URL}lat={lat}&lon={lon}&appid={API_key}')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching pollution data for {city['name']} (lat={lat}, lon={lon}): {error}")
            return None

    def get_pollution_history(self, city: dict, start_data: str, end_data: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve historical air quality data for the city between specified dates.

        :param city: Dictionary containing city data with keys "name", "lat", "lon".
        :param start_data: Start date in the format "dd/mm/yyyy".
        :param end_data: End date in the format "dd/mm/yyyy".
        :return: Dictionary containing historical air quality data or None if an error occurs.
        """
        lat, lon = city['lat'], city['lon']
        start_data_unix = string_data_to_timestamp_unix(start_data)
        end_data_unix = string_data_to_timestamp_unix(end_data)

        try:
            response = self.session.get(
                f'{URLs.AIR_POLLUTION_HISTORY_URL}lat={lat}&lon={lon}&start={start_data_unix}&end={end_data_unix}&appid={API_key}')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching pollution history for {city['name']} (lat={lat}, lon={lon}): {error}")
            return None

    def get_weather_current(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve current weather data for the city.

        :param city_name: Name of the city.
        :return: Dictionary containing current weather data or None if an error occurs.
        """
        try:
            response = self.session.get(f'{URLs.WEATHER_CURRENT_URL}q={city_name}&appid={API_key}&units=metric')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching weather data for {city_name}: {error}")
            return None

    def get_weather_forecast_daily(self, city: dict) -> Optional[Dict[str, Any]]:
        """
        Retrieve daily weather forecast for the city for the next day.

        :param city: Dictionary containing city data with keys "name", "lat", "lon".
        :return: Dictionary containing daily weather forecast or None if an error occurs.
        """
        lat, lon = city['lat'], city['lon']
        try:
            response = self.session.get(
                f'{URLs.WEATHER_DAILY_FORECAST_URL}lat={lat}&lon={lon}&cnt=1&appid={API_key}&units=metric')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching weather forecast for {city['name']} (lat={lat}, lon={lon}): {error}")
            return None

    def retrive_data(self):
        """
        Fetch and return data for all cities listed in the configuration file.
        """
        results = {}
        for city in self.cities:
            results[city["name"]] = {
                "coordinates": {"lat": city["lat"], "lon": city["lon"]},
                "pollution": self.get_pollution(city),
                "current_weather": self.get_weather_current(city["name"]),
            }
        return results

    def close_session(self) -> None:
        """
        Close the session to clean up resources.
        """
        self.session.close()

