import cerberus
from . import locations_file

schema = {
    "document": {
        "type": "dict",
        "keysrules": {"type": "string", "regex": "^[a-zA-Z0-9_-]{1,16}$"},
        "valuesrules": {
            "type": "dict",
            "schema": {
                "details": {"type": "string"},
                "lat": {"type": "number", "min": -90, "max": 90},
                "lon": {"type": "number", "min": -180, "max": 180},
                "alt": {"type": "number", "min": 0, "max": 3000},
            },
        },
    }
}

example_document = {
    "BRU": {
        "details": "Industriegelände an der Brudermühlstraße",
        "lat": 48.111,
        "lon": 11.547,
        "alt": 528,
    }
}


def test_location_coordinates_integrity(locations_file):
    v = cerberus.Validator(schema)
    assert v.validate({"document": example_document})
    print("Cerberus errors 1: ", v.errors)

    assert v.validate({"document": locations_file})
    print("Cerberus errors 2: ", v.errors)
