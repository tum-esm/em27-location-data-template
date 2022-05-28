from datetime import datetime
import json
import os
import pytest

dir = os.path.dirname
PROJECT_DIR = dir(dir(dir(os.path.abspath(__file__))))


def _load_json_file(filename: str):
    filepath = os.path.join(PROJECT_DIR, "data", filename)
    assert os.path.isfile(filepath), f"{filename} file does not exist"
    with open(filepath, "r") as f:
        document = json.load(f)
    return document


def check_date_value(field, value, error):
    if value is not None:
        try:
            datetime.strptime(str(value), "%Y%m%d")
        except ValueError:
            error(field, "value is not a valid date")


@pytest.fixture
def locations_file():
    return _load_json_file("locations.json")


@pytest.fixture
def sensors_file():
    return _load_json_file("sensors.json")


@pytest.fixture
def campaigns_file():
    return _load_json_file("campaigns.json")
