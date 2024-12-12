import functions_framework
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # add gcloud_functions to system paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add root folder to system paths

from extract.extract import Extract
from extract.strategies.open_weather_strategy import OpenweatherDataExtractor



@functions_framework.http
def fetch_openweather_data(request, context=None):
    openweather_strategy = OpenweatherDataExtractor()
    extract_object = Extract(
        strategy=openweather_strategy
    )

    return str(extract_object.retrieve_data())



