from datetime import datetime, timedelta
import json
import logging
from time import sleep

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


def structure_center_details(center):
    sessions = center.pop("sessions", [])
    _ = center.pop("vaccine_fees", [])
    center_sessions = []
    for session in sessions:
        if session["min_age_limit"] < 45:
            center_copy = center.copy()
            center_copy["id"] = session["session_id"]
            center_copy.update(session)
            center_sessions.append(center_copy)

    return center_sessions


def query_available_centers(district_id):
    date = datetime.now() + timedelta(days=1)
    date_str = date.strftime("%d-%m-%Y")
    try:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={district_id}&date={date_str}"
        r = requests.get(url)
        logger.info(f"{district_id} - {r}")
        data = r.json()
        centers = [
            center
            for center in data["centers"]
            if any(session["min_age_limit"] < 45 for session in center["sessions"])
        ]
        center_details = []
        for center in centers:
            center_details.extend(structure_center_details(center))

        return center_details
    except:
        logger.error(f"Error in fetching for district - {district_id}")


@app.task
def fetch_district(district_id):
    sleep(1)
    logger.info(f"Fetching for district - {district_id}")
    centers = query_available_centers(district_id)
    redis.set(DISTRICT_KEY(district_id), json.dumps(centers))
