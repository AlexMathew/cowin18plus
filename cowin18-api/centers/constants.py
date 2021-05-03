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
            DISTRICTS_DATA[state["state_id"]] = [
                {"state_id": state["state_id"], **district}
                for district in districts["districts"]
            ]

LIVE_UPDATES_DISTRICT_IDS = [
    # 571,  # Chennai
]

DISTRICT_KEY = lambda district_id: f"DISTRICT_{district_id}"
DISTRICT_UPDATE_TIME_KEY = lambda district_id: f"DISTRICT_UPDATED_{district_id}"
