import json
import base64
from datetime import datetime

import functions_framework
import sys
import os

from google.cloud import pubsub_v1, bigquery

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # add gcloud_functions to system paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add root folder to system paths

from extract.extract import Extract
from extract.strategies.open_weather_strategy import OpenweatherDataExtractor



@functions_framework.http
def fetch_openweather_data(request, context=None):
    print()
    openweather_strategy = OpenweatherDataExtractor()
    extract_object = Extract(
        strategy=openweather_strategy
    )
    data = extract_object.retrieve_data()
    print(json.dumps(data, indent=2))
    data_str = json.dumps(data)
    data_bytes = data_str.encode("utf-8") #error - str
    publisher = pubsub_v1.PublisherClient()
    project_id = "corded-shadow-429909-b2"
    topic_id = "airpollution-topic"
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, data_bytes)
    print(f"Published message ID: {future.result()}")

    # return str(extract_object.retrieve_data())
    return "True", 200



@functions_framework.cloud_event
def example_function(cloud_event):
    message = cloud_event.data["message"]['data']
    decoded_message = base64.b64decode(message).decode('utf-8')
    raw_data = json.loads(decoded_message)
    row_to_insert = []
    for city, data in raw_data.items():
        try:
            weather = data["current_weather"]
            pollution = data["pollution"]["list"][0]["components"]
            pollution_main = data["pollution"]["list"][0]["main"]
            record = {
                "city": city,
                "timestamp": datetime.fromtimestamp(weather["dt"]).isoformat() + "Z",
                "temp": weather["main"]["temp"],
                "humidity": weather["main"]["humidity"],
                "pressure": weather["main"]["pressure"],
                "wind_speed": weather["wind"]["speed"],
                "aqi": pollution_main["aqi"],
                "pm10": pollution["pm10"],
                "pm2_5": pollution["pm2_5"],
                "no2": pollution["no2"],
                "co": pollution["co"],
                "lat": data["coordinates"]["lat"],
                "lon": data["coordinates"]["lon"]
            }
            row_to_insert.append(record)
        except Exception as e:
            print(f"Error processing data for {city}: {e}")
            continue


    client = bigquery.Client()
    table_id = "corded-shadow-429909-b2.air_pollution_data.weather_pollution_data"
    errors = client.insert_rows_json(table_id, row_to_insert)


    if errors:
        return "False", 500

    print(row_to_insert)
    print("Data inserted successfully")
    return "True", 200


"""
request -> data -> reformat data -> use bigquery client -> insert data to bigquery
"""



'''
  WORKFLOW : fetch_openweather_data() -> send data to topic -> automatyczna egzekucja funkcji example_funciton() -> print Hello
  
  ===========================
  
  1. Stworzenie topicu w GCP    
  
  2. Poprawienie funkcji fetch_openweather_data():
    - wysyla `data` do topicu
    
  3. Deployment drugiej funkcji event based:
    - zsynchronizowana z topic do ktorego fetch_openweather_data() wysyla dane
  
  4. Test calego workflow
'''



