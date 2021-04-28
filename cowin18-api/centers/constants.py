import os
import json

directory = os.path.dirname(__file__)

# DISTRICT_IDS = []
# with open(os.path.join(directory, "districts/states.json")) as f:
#     states = json.load(f)
#     for state in states["states"]:
#         if state["state_name"] in ["Tamil Nadu"]:
#             with open(
#                 os.path.join(directory, f"districts/{state['state_id']}.json")
#             ) as f:
#                 districts = json.load(f)
#                 district_ids = [
#                     district["district_id"] for district in districts["districts"]
#                 ]
#                 DISTRICT_IDS.extend(district_ids)
DISTRICT_IDS = [
    571,  # Chennai
    265,  # Bangalore Urban
    395,  # Mumbai
    307,  # Ernakulam
    140,  # New Delhi
    581,  # Hyderabad
    725,  # Kolkata
]

DISTRICT_KEY = lambda district_id: f"DISTRICT_{district_id}"
