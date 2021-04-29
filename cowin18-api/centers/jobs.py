from datetime import datetime, timedelta
import json
import logging
from time import sleep

import requests
import redis
from django.conf import settings

from cowin18.celery import app
from helpers.instances import redis

from .constants import (
    DISTRICT_IDS,
    DISTRICT_KEY,
    DISTRICT_UPDATE_TIME_KEY,
    LOCAL_NGROK_URL,
)

logger = logging.getLogger(__name__)


@app.task(name="cowin18.fetch_available_centers")
def fetch_available_centers():
    if settings.IS_SERVER:
        logger.info("fetch_available_centers will not be run on the server")
        return

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
    if centers is not None:
        redis.set(DISTRICT_KEY(district_id), json.dumps(centers))
        redis.set(DISTRICT_UPDATE_TIME_KEY(district_id), datetime.now().strftime("%c"))


"""
Super hacky stuff. We can't make requests to the CoWin endpoint from AWS. 
So instead, I'm not running it locally, then querying the local API and populating
in prod from that.
"""


@app.task(name="cowin18.fetch_data_from_local")
def fetch_data_from_local():
    if settings.IS_SERVER:
        url = f"{LOCAL_NGROK_URL}/api/v1/centers/"
        r = requests.get(url)
        data = r.json()
        for district, centers in data["centers"].items():
            redis.set(district, json.dumps(centers))
        for district, updated in data["updated"].items():
            redis.set(district, updated)
