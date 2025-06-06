from datetime import timezone, datetime
import yaml
import os

def load_config() -> list:
    """
    Load city names from a YAML configuration file.

    :param config_path: Full path to the YAML configuration file.
    :return: List of city names.
    """
    config_path = os.getcwd().strip("utils") + "config\\cities_config.yaml"
    config_path = os.getcwd().strip("utils") + "\\utils\\config\\cities_config.yaml"
    # config_path = config_path.replace('\\', '/')
    # config_path = "./utils/config/cities_config.yaml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    if "cities" not in config or not isinstance(config["cities"], list):
        raise ValueError("The YAML configuration file must contain a 'cities' key with a list of cities.")
    return config["cities"]


def string_data_to_timestamp_unix(data: str):
    """
    Convert a date string in dd/mm/yyyy format to Unix timestamp (UTC).

    :param data: Date string in the format "dd/mm/yyyy".
    :return: Corresponding Unix timestamp as an integer.
    """
    return int(datetime.strptime(data, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())


# config_path = os.getcwd().strip("utils") + "\\utils\\config\\cities_config.yaml"
# config_path = config_path.replace('\\', '/')
# print(config_path)