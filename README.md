# EM27 Location Data

This repository serves as a the single source of truth for EM27 measurement logistics: "Where has each station been on each day of measurements?" We selected this format over placing it in a database due to various reasons:

-   Easy to read, modify and extend by selective group members using GitHub permissions
-   Changes to this are more obvious here than in database logs
-   Versioning makes it easy to revert mistakes
-   Simple offline usability for stations without an internet connection
-   Automatic testing of the files integrities

<br/>

## What does this data look like?

There is a set of locations in **`data/locations.json`**:

```json
{
    "BRU": {
        "details": "Industriegelände an der Brudermühlstraße",
        "lon": 11.547,
        "lat": 48.111,
        "alt": 528
    },
    "DLR": {
        "details": "DLR in Wessling",
        "lon": 11.279,
        "lat": 48.086,
        "alt": 592
    }
}
```

There is a set of sensors in **`data/sensors.json`** that measure at these location sites:

```json
{
    "ma": {
        "serialNumber": 61,
        "locations": [
            { "from": 20181019, "to": 20181019, "location": "TUM_LAB" },
            { "from": 20181020, "to": 20181030, "location": "LMU" },
            { "from": 20181031, "to": 20220515, "location": "TUM_I" }
        ]
    },
    "mb": {
        "serialNumber": 86,
        "locations": [
            { "from": 20210913, "to": 20210930, "location": "TUM_I" },
            { "from": 20211001, "to": 20220513, "location": "FEL" },
            { "from": 20220514, "to": 20220515, "location": "TUM_I" }
        ]
    }
}
```

There is a set of campaigns in **`data/campaigns.json`**:

```json
{
    "muccnet": {
        "from": 20190913,
        "to": 21000101,
        "stations": [
            {
                "sensor": "ma",
                "defaultLocation": "TUM_I",
                "direction": "center"
            },
            { "sensor": "mb", "defaultLocation": "FEL", "direction": "east" },
            { "sensor": "mc", "defaultLocation": "GRAE", "direction": "west" },
            { "sensor": "md", "defaultLocation": "OBE", "direction": "north" },
            { "sensor": "me", "defaultLocation": "TAU", "direction": "south" }
        ]
    }
}
```

<br/>

## How to add new measurement days?

1. Possibly add new locations in `data/locations.json`
2. Extend the list of locations in `data/sensors.json`
3. Possibly add new campaign setups in `data/campaigns.json`

<br/>

## How can I know whether my changes were correct?

Whenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed in the "actions" tab of your repository.

A list of all integrity tests can be found in `integrity-tests/README.md`
