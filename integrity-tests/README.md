# Integrity tests of the JSON files

These tests are set up to run on every push to the repository.

## Conducted tests

**`test_locations.py`:**

-   JSON file exists
-   JSON format is valid
-   Values for `lat`/`lng`/`alt` are in a reasonable range

**`test_sensors.py`:**

-   JSON file exists
-   JSON format is valid
-   All dates exist
-   Time periods are ordered ascendingly
-   no overlapping time periods
-   no gaps between time periods
-   last time periods ends with null
-   no two adjacent time periods with the same location
-   all locations exist in `location-coordinates`

**`test_campaigns.py`:**

-   JSON file exists
-   JSON format is valid
-   All dates exist
-   start date before end date
-   no duplicate sensors/locations/directions
-   directions make sense (lat of north > lat of south)
-   locations in `location-coordinates`
-   sensors in `sensor-locations`

## Run tests

```bash
cd integrity-tests

# create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# install dependencies using poetry (https://python-poetry.org/)
poetry install

# run integrity tests using pytest
pytest tests
```
