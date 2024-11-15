import functions_framework
from utils.URLs import WEATHER_DAILY_FORECAST_URL

@functions_framework.http
def fetch_openweather_data(request, context=None):
    print('Hello World')
    print(WEATHER_DAILY_FORECAST_URL)