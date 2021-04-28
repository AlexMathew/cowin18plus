import json

from rest_framework.views import APIView
from rest_framework.response import Response

from helpers.instances import redis

from .constants import DISTRICT_IDS, DISTRICT_KEY


class CentersListView(APIView):
    def get(self, request):
        data = {
            DISTRICT_KEY(district_id): json.loads(
                redis.get(DISTRICT_KEY(district_id)) or "null"
            )
            for district_id in DISTRICT_IDS
        }
        return Response(data)
