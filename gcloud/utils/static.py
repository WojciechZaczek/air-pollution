from datetime import timezone, datetime
import yaml


def load_config(config_path) -> list:
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


def string_data_to_timestamp_unix(data: str):
    """
    Convert a date string in dd/mm/yyyy format to Unix timestamp (UTC).

    :param data: Date string in the format "dd/mm/yyyy".
    :return: Corresponding Unix timestamp as an integer.
    """
    return int(datetime.strptime(data, "%d/%m/%Y").replace(tzinfo=timezone.utc).timestamp())