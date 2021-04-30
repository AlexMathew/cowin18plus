import os
import json

directory = os.path.dirname(__file__)

STATES_DATA = []
DISTRICTS_DATA = {}

with open(os.path.join(directory, "districts/states.json")) as f:
    states = json.load(f)
    STATES_DATA = states["states"]
    for state in STATES_DATA:
        with open(os.path.join(directory, f"districts/{state['state_id']}.json")) as f:
            districts = json.load(f)
            district_ids = [
                district["district_id"] for district in districts["districts"]
            ]
            DISTRICTS_DATA[state["state_id"]] = districts["districts"]

DISTRICT_KEY = lambda district_id: f"DISTRICT_{district_id}"
DISTRICT_UPDATE_TIME_KEY = lambda district_id: f"DISTRICT_UPDATED_{district_id}"
