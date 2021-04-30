import json
import itertools

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from helpers.instances import redis

from .constants import (
    STATES_DATA,
    DISTRICTS_DATA,
    DISTRICT_KEY,
    DISTRICT_UPDATE_TIME_KEY,
)


class DistrictsListView(APIView):
    def get(self, request):
        data = {
            "states": STATES_DATA,
            "districts": DISTRICTS_DATA,
        }

        return Response(data)


class CentersListView(APIView):
    def get(self, request):
        state_id = request.query_params.get("stateId")
        if not state_id:
            return Response(
                {"error": "`stateId` query param should be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {}

        try:
            districts = DISTRICTS_DATA[int(state_id)]
            district_ids = [district["district_id"] for district in districts]
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

        except (KeyError, ValueError):
            return Response(
                {"error": "Invalid `stateId`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(data)


class CentersListV1View(APIView):
    def get(self, request):
        district_ids = list(
            itertools.chain(
                *[
                    [
                        district["district_id"]
                        for district in DISTRICTS_DATA[state["state_id"]]
                    ]
                    for state in STATES_DATA
                ]
            )
        )

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
            "districts": [],
            "updated": updated,
            "centers": centers,
        }
        return Response(data)
