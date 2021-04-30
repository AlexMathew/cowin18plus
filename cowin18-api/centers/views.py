import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response

from helpers.instances import redis

from .constants import (
    DISTRICT_IDS,
    DISTRICT_KEY,
    DISTRICT_IDS_AND_DISTRICTS,
    DISTRICT_UPDATE_TIME_KEY,
)

directory = os.path.dirname(__file__)


class DistrictsListView(APIView):
    def get(self, request):
        data = {
            "states": [],
            "districts": {},
        }
        with open(os.path.join(directory, "districts/states.json")) as f:
            states = json.load(f)
            data["states"] = states["states"]
            for state in states["states"]:
                with open(
                    os.path.join(directory, f"districts/{state['state_id']}.json")
                ) as f:
                    districts = json.load(f)
                    data["districts"][state["state_id"]] = districts["districts"]

        return Response(data)


class CentersListView(APIView):
    def get(self, request):
        centers = {
            DISTRICT_KEY(district_id): sorted(
                json.loads(redis.get(DISTRICT_KEY(district_id)) or "[]"),
                key=lambda center: center["name"],
            )
            for district_id in DISTRICT_IDS
        }
        updated = {
            DISTRICT_UPDATE_TIME_KEY(district_id): (
                (redis.get(DISTRICT_UPDATE_TIME_KEY(district_id)) or b"").decode(
                    "utf-8"
                )
                or None
            )
            for district_id in DISTRICT_IDS
        }
        data = {
            "districts": DISTRICT_IDS_AND_DISTRICTS,
            "updated": updated,
            "centers": centers,
        }
        return Response(data)
