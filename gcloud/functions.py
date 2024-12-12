from datetime import timezone, datetime
from pathlib import Path
import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException
import yaml
from weather_API_key import API_key
from utils import URLs


class APIAirPollution:

    def __init__(self) -> None:
        """
        Initialize the APIAirPollution object with a persistent HTTP session
        and city configuration loaded from a YAML file.
        """
        config_path = Path(__file__).resolve().parent.parent / "utils" / "config" / "cities_config.yaml"
        self.cities = self.load_config(config_path)

        self.session = requests.Session()

    @staticmethod
    def load_config(config_path: str) -> list:
        """
        Load city names from a YAML configuration file.

        :param config_path: Full path to the YAML configuration file.
        :return: List of city names.
        """
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        if "cities" not in config or not isinstance(config["cities"], list):
            raise ValueError("The YAML configuration file must contain a 'cities' key with a list of cities.")
        return config["cities"]

    @staticmethod
    def string_data_to_timestamp_unix(data: str) -> int:
        """
        Convert a date string in dd/mm/yyyy format to Unix timestamp (UTC).

        :param data: Date string in the format "dd/mm/yyyy".
        :return: Corresponding Unix timestamp as an integer.
        """
        return int(datetime.strptime(data, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())

    def get_coordinates(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve geographic coordinates of the city using the geolocation API.

        :param city_name: Name of the city.
        :return: Dictionary containing latitude and longitude or None if the city is not found.
        """
        try:
            response = self.session.get(f'{URLs.GEO_DIRECT_URL}q={city_name}&appid={API_key}')
            response.raise_for_status()
            return response.json()[0]
        except (RequestException, IndexError) as error:
            print(f"Error fetching coordinates for {city_name}: {error}")
            return None

    def get_pollution(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve current air quality data for the specified city.

        :param city_name: Name of the city.
        :return: Dictionary containing air pollution data or None if an error occurs.
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            print(f"Could not fetch coordinates for {city_name}. Skipping pollution data.")
            return None

        lat, lon = coords['lat'], coords['lon']
        try:
            response = self.session.get(f'{URLs.AIR_POLLUTION_URL}lat={lat}&lon={lon}&appid={API_key}')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching pollution data for {city_name} (lat={lat}, lon={lon}): {error}")
            return None

    def get_pollution_history(self, city_name: str, start_data: str, end_data: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve historical air quality data for the city between specified dates.

        :param city_name: Name of the city.
        :param start_data: Start date in the format "dd/mm/yyyy".
        :param end_data: End date in the format "dd/mm/yyyy".
        :return: Dictionary containing historical air quality data or None if an error occurs.
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            print(f"Could not fetch coordinates for {city_name}. Skipping history data.")
            return None

        lat, lon = coords['lat'], coords['lon']
        start_data_unix = self.string_data_to_timestamp_unix(start_data)
        end_data_unix = self.string_data_to_timestamp_unix(end_data)

        try:
            response = self.session.get(
                f'{URLs.AIR_POLLUTION_HISTORY_URL}lat={lat}&lon={lon}&start={start_data_unix}&end={end_data_unix}&appid={API_key}')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching pollution history for {city_name}: {error}")
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

    def get_weather_forecast_daily(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve daily weather forecast for the city for the next day.

        :param city_name: Name of the city.
        :return: Dictionary containing daily weather forecast or None if an error occurs.
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            print(f"Could not fetch coordinates for {city_name}. Skipping weather forecast.")
            return None

        lat, lon = coords['lat'], coords['lon']
        try:
            response = self.session.get(
                f'{URLs.WEATHER_DAILY_FORECAST_URL}lat={lat}&lon={lon}&cnt=1&appid={API_key}&units=metric')
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(f"Error fetching weather forecast for {city_name}: {error}")
            return None

    def fetch_data_for_all_cities(self) -> Dict[str, Dict[str, Any]]:
        """
        Fetch and print data for all cities listed in the configuration file.
        """
        results = {}
        for city in self.cities:
            results[city] = {
                "coordinates": self.get_coordinates(city),
                "pollution": self.get_pollution(city),
                "current_weather": self.get_weather_current(city),
                "forecast": self.get_weather_forecast_daily(city)
            }
        return results

    def close_session(self) -> None:
        """
        Close the session to clean up resources.
        """
        self.session.close()


if __name__ == "__main__":
    api = APIAirPollution()
    try:
        results = api.fetch_data_for_all_cities()
        for city, data in results.items():
            print(f"{city}: {data}")
    finally:
        api.close_session()

