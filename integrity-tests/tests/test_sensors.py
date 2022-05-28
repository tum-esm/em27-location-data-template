from datetime import datetime
import cerberus
from . import sensors_file, locations_file, check_date_value

schema = {
    "document": {
        "type": "dict",
        "keysrules": {"type": "string", "regex": "^[a-zA-Z0-9_-]{1,16}$"},
        "valuesrules": {
            "type": "dict",
            "schema": {
                "serialNumber": {"type": "integer"},
                "locations": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "from": {"type": "integer", "check_with": check_date_value},
                            "to": {"type": "integer", "check_with": check_date_value},
                            "location": {"type": "string"},
                        },
                    },
                },
            },
        },
    }
}

example_document = {
    "ma": {
        "serialNumber": 61,
        "locations": [{"from": 20210101, "to": 21000101, "location": "TUM_I"}],
    },
}


def test_sensor_locations_integrity(sensors_file, locations_file):

    v = cerberus.Validator(schema)
    validation_result_1 = v.validate({"document": example_document})
    print("Cerberus errors 1: ", v.errors)
    assert validation_result_1

    validation_result_2 = v.validate({"document": sensors_file})
    print("Cerberus errors 2: ", v.errors)
    assert validation_result_2

    serial_numbers = []

    for sensor in sensors_file.keys():

        sensor_time_periods = sensors_file[sensor]["locations"]
        period_count = len(sensor_time_periods)
        assert period_count > 0, f'["{sensor}"]: time period list is empty'

        sn = sensors_file[sensor]["serialNumber"]
        assert sn not in serial_numbers, f"duplicate serial number {sn}"
        serial_numbers.append(sn)

        for i in range(period_count):
            try:
                assert (
                    sensor_time_periods[i]["from"] <= sensor_time_periods[i]["to"]
                ), '"from" has to be less equal "to"'
                assert (
                    sensor_time_periods[i]["location"] in locations_file.keys()
                ), "location does not have coordinates"
                if i < period_count - 1:
                    assert (
                        datetime.strptime(
                            str(sensor_time_periods[i + 1]["from"]), "%Y%m%d"
                        )
                        - datetime.strptime(str(sensor_time_periods[i]["to"]), "%Y%m%d")
                    ).days == 1, "gap between periods is not exactly 1 day"
                    assert (
                        sensor_time_periods[i]["location"]
                        != sensor_time_periods[i + 1]["location"]
                    ), "same location in adjacent period"
            except AssertionError as e:
                raise Exception(f'["{sensor}"][{i}]: {e}')
