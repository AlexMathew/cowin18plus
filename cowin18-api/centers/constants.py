import os
import json

directory = os.path.dirname(__file__)

DISTRICT_IDS = []
with open(os.path.join(directory, "districts/states.json")) as f:
    states = json.load(f)
    for state in states["states"]:
        with open(os.path.join(directory, f"districts/{state['state_id']}.json")) as f:
            districts = json.load(f)
            district_ids = [
                district["district_id"] for district in districts["districts"]
            ]
            DISTRICT_IDS.extend(district_ids)


DISTRICT_KEY = lambda district_id: f"DISTRICT_{district_id}"
