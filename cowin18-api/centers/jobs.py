from datetime import datetime, timedelta
import json
import logging

import requests
import redis

from cowin18.celery import app
from helpers.instances import redis

from .constants import (
    STATES_DATA,
    DISTRICTS_DATA,
    DISTRICT_KEY,
    DISTRICT_UPDATE_TIME_KEY,
    LIVE_UPDATES_DISTRICT_IDS,
)

logger = logging.getLogger(__name__)


@app.task(name="cowin18.fetch_available_centers")
def fetch_available_centers():
    logger.info("fetch_available_centers")
    for state in STATES_DATA:
        for district in DISTRICTS_DATA[state["state_id"]]:
            fetch_district.apply_async(
                (district["district_id"],),
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
        base_url = (
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"
            if district_id in LIVE_UPDATES_DISTRICT_IDS
            else "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
        )
        query_params = f"?district_id={district_id}&date={date_str}"
        url = f"{base_url}{query_params}"
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
    logger.info(f"Fetching for district - {district_id}")
    centers = query_available_centers(district_id)
    if centers is not None:
        redis.set(DISTRICT_KEY(district_id), json.dumps(centers))
        redis.set(DISTRICT_UPDATE_TIME_KEY(district_id), datetime.now().strftime("%c"))


# """
# Super hacky stuff. We can't make requests to the CoWin endpoint from AWS.
# So instead, I'm not running it locally, then querying the local API and populating
# in prod from that.
# """


# @app.task(name="cowin18.fetch_data_from_local")
# def fetch_data_from_local():
#     if settings.IS_SERVER:
#         url = f"{LOCAL_NGROK_URL}/api/v1/centers/"
#         r = requests.get(url)
#         data = r.json()
#         for district, centers in data["centers"].items():
#             redis.set(district, json.dumps(centers))
#         for district, updated in data["updated"].items():
#             redis.set(district, updated)
