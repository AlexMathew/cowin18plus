import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from helpers.instances import redis

from .constants import (
    DISTRICT_KEY,
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
        state_id = request.query_params["state_id"]
        if not state_id:
            return Response(
                {"error": "`state_id` query param should be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {}

        try:
            with open(os.path.join(directory, f"districts/{state_id}.json")) as f:
                districts = json.load(f)
                district_ids = [
                    district["district_id"] for district in districts["districts"]
                ]
            centers = {
                DISTRICT_KEY(district_id): sorted(
                    json.loads(redis.get(DISTRICT_KEY(district_id)) or "[]"),
                    key=lambda center: center["name"],
                )
                for district_id in district_ids
            }
            updated = {
                DISTRICT_UPDATE_TIME_KEY(district_id): (
                    (redis.get(DISTRICT_UPDATE_TIME_KEY(district_id)) or b"").decode(
                        "utf-8"
                    )
                    or None
                )
                for district_id in district_ids
            }
            data = {
                "updated": updated,
                "centers": centers,
            }

        except FileNotFoundError:
            return Response(
                {"error": "Invalid `state_id`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(data)
