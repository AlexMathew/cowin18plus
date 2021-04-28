from datetime import datetime, timedelta
import json
import logging

import requests
import redis

from cowin18.celery import app
from helpers.instances import redis

from .constants import DISTRICT_IDS, DISTRICT_KEY

logger = logging.getLogger(__name__)


@app.task(name="cowin18.fetch_available_centers")
def fetch_available_centers():
    logger.info("fetch_available_centers")
    for district_id in DISTRICT_IDS:
        fetch_district.apply_async(
            (district_id,),
        )


def query_available_centers(district_id):
    date = datetime.now() + timedelta(days=1)
    date_str = date.strftime("%d-%m-%Y")
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={district_id}&date={date_str}"
    r = requests.get(url)
    data = r.json()
    centers = [
        center
        for center in data["centers"]
        if any(session["min_age_limit"] < 45 for session in center["sessions"])
    ]
    return centers


@app.task
def fetch_district(district_id):
    logger.info(f"Fetching for district - {district_id}")
    centers = query_available_centers(district_id)
    redis.set(DISTRICT_KEY(district_id), json.dumps(centers))