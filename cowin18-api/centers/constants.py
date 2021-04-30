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

DISTRICT_IDS_AND_DISTRICTS = sorted(
    [
        {"id": 571, "name": "Chennai"},
        # {"id": 265, "name": "Bangalore Urban"},
        # {"id": 395, "name": "Mumbai"},
        # {"id": 307, "name": "Ernakulam"},
        # {"id": 140, "name": "New Delhi"},
        # {"id": 581, "name": "Hyderabad"},
        # {"id": 725, "name": "Kolkata"},
    ],
    key=lambda district: district["name"],
)
# DISTRICT_IDS = [district["id"] for district in DISTRICT_IDS_AND_DISTRICTS]

DISTRICT_KEY = lambda district_id: f"DISTRICT_{district_id}"
DISTRICT_UPDATE_TIME_KEY = lambda district_id: f"DISTRICT_UPDATED_{district_id}"

LOCAL_NGROK_URL = ""
