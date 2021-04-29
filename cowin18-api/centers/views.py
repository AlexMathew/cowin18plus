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


class CentersListView(APIView):
    def get(self, request):
        centers = {
            DISTRICT_KEY(district_id): json.loads(
                redis.get(DISTRICT_KEY(district_id)) or "null"
            )
            for district_id in DISTRICT_IDS
        }
        updated = {
            DISTRICT_UPDATE_TIME_KEY(district_id): (
                redis.get(DISTRICT_UPDATE_TIME_KEY(district_id)).decode("utf-8") or None
            )
            for district_id in DISTRICT_IDS
        }
        data = {
            "districts": DISTRICT_IDS_AND_DISTRICTS,
            "updated": updated,
            "centers": centers,
        }
        return Response(data)
