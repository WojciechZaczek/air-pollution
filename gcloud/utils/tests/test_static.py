import pytest
import yaml

from gcloud.utils.static import string_data_to_timestamp_unix, load_config


class TestDataToTimestamp:
    @classmethod
    def setup_class(cls):
        cls.date_str = "12/12/2024"

    def test_string_data_to_timestamp_unix_returns_correct_value(self):
        expected_timestamp = 1733961600
        assert string_data_to_timestamp_unix(self.date_str) == expected_timestamp

    def test_string_data_to_timestamp_unix_with_incorrect_argument_returns_returns_error_value(self):
        with pytest.raises(ValueError):
            string_data_to_timestamp_unix("12-12-2024")

    def test_string_data_to_timestamp_unix_with_empty_argument_returns_returns_error_value(self):
        with pytest.raises(ValueError):
            string_data_to_timestamp_unix("")


class TestLoadConfig:
    def test_load_config_returns_valid_data(self, tmp_path):
        config_content = {"cities": ["New York", "Los Angeles", "Chicago"]}
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as file:
            yaml.dump(config_content, file)

        result = load_config(config_path)
        assert result == ["New York", "Los Angeles", "Chicago"]

    def test_load_config_with_confing_file_missing_cities_key_returns_error(self, tmp_path):
        config_content = {"countries": ["USA", "Canada"]}
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as file:
            yaml.dump(config_content, file)

        with pytest.raises(ValueError,
                           match="The YAML configuration file must contain a 'cities' key with a list of cities."
                           ):
            load_config(config_path)


