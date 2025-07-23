import functions_framework
import sys
import os
from google.cloud import pubsub_v1

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
    data = data.encode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    project_id = "corded-shadow-429909-b2"
    topic_id = "airpolution-topic"
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

    # return str(extract_object.retrieve_data())
    return "True", 200

# https://cloud.google.com/functions/docs/deploy
@functions_framework.cloud_event
def example_function(request, context=None):
    print("Hello")
    return "True", 200


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



'''
from google.cloud import pubsub_v1
from google.oauth2 import service_account

# Ścieżka do pliku klucza konta usługowego
key_path = "key/pubsub-demo-438714-f39390e5cf71.json"

# Ustawienia klienta pubsub z uwierzytelnianiem
credentials = service_account.Credentials.from_service_account_file(key_path)
publisher = pubsub_v1.PublisherClient(credentials=credentials)

# Ustawienia projektu i tematu
project_id = "pubsub-demo-438714"
topic_id = "pubsub-topic-demo"
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message():
    data = "Hello, world!"
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    publish_message
'''

