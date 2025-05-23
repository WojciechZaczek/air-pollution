import functions_framework
import sys
import os

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
    # stworzyc publisher client publisher = pubsub_v1.PublisherClient()
    # wysłać dane za pomocą publisher.publish(topic_path, data)
    return str(extract_object.retrieve_data())




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

