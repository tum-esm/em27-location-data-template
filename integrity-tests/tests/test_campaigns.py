import cerberus
from . import (
    campaigns_file,
    locations_file,
    sensors_file,
    check_date_value,
)

schema = {
    "document": {
        "type": "dict",
        "keysrules": {"type": "string", "regex": "^[a-zA-Z0-9_-]{1,32}$"},
        "valuesrules": {
            "type": "dict",
            "schema": {
                "from": {"type": "integer", "check_with": check_date_value},
                "to": {"type": "integer", "check_with": check_date_value},
                "stations": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "sensor": {"type": "string"},
                            "defaultLocation": {"type": "string"},
                            "direction": {
                                "type": "string",
                                "allowed": ["north", "east", "south", "west", "center"],
                            },
                        },
                    },
                },
            },
        },
    }
}

example_document = {
    "example": {
        "from": 20190913,
        "to": 21000101,
        "stations": [
            {"sensor": "ma", "defaultLocation": "TUM_I", "direction": "center"},
            {"sensor": "mb", "defaultLocation": "FEL", "direction": "east"},
        ],
    },
}


def unique(xs):
    new_xs = []
    for x in list(xs):
        if x not in new_xs:
            new_xs.append(x)
    return new_xs


def test_campaign_setups(campaigns_file, locations_file, sensors_file):
    v = cerberus.Validator(schema)
    assert v.validate({"document": example_document})
    print("Cerberus errors 1: ", v.errors)

    assert v.validate({"document": campaigns_file})
    print("Cerberus errors 2: ", v.errors)

    for campaign, setup in campaigns_file.items():
        try:
            assert setup["from"] <= setup["to"], '"from" greater than "to"'
            assert len(setup["stations"]) > 0, "station list is empty"

            locations = unique(map(lambda x: x["defaultLocation"], setup["stations"]))
            sensors = unique(map(lambda x: x["sensor"], setup["stations"]))
            directions = unique(map(lambda x: x["direction"], setup["stations"]))

            assert len(locations) == len(
                setup["stations"]
            ), "same location used for multiple stations"
            assert len(sensors) == len(
                setup["stations"]
            ), "same sensor used for multiple stations"
            assert len(directions) == len(
                setup["stations"]
            ), "same direction used for multiple stations"

            for location in locations:
                assert (
                    location in locations_file.keys()
                ), f'location "{location}" has no coordinates'

            for sensor in sensors:
                assert (
                    sensor in sensors_file.keys()
                ), f'sensor "{sensor}" has no location records'

            direction_coordinates = {}
            for station in setup["stations"]:
                direction_coordinates[station["direction"]] = locations_file[
                    station["defaultLocation"]
                ]

            try:
                latitudes = [c["lat"] for c in direction_coordinates.values()]
                longitudes = [c["lon"] for c in direction_coordinates.values()]
                if "north" in direction_coordinates.keys():
                    assert direction_coordinates["north"]["lat"] == max(latitudes)
                if "south" in direction_coordinates.keys():
                    assert direction_coordinates["south"]["lat"] == min(latitudes)
                if "east" in direction_coordinates.keys():
                    assert direction_coordinates["east"]["lon"] == max(longitudes)
                if "west" in direction_coordinates.keys():
                    assert direction_coordinates["west"]["lon"] == min(longitudes)
            except:
                print(f"direction_coordinates: {direction_coordinates}")
                raise AssertionError("direction_coordinates do not make sense")
        except AssertionError as e:
            raise Exception(f'["{campaign}"]: {e}')
