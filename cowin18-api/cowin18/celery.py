from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cowin18.settings")

REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"

app = Celery("cowin18")

app.conf.broker_url = REDIS_URL
app.conf.result_expires = 3600
app.conf.timezone = settings.TIME_ZONE
app.conf.imports = "centers.jobs"
app.conf.beat_schedule = {
    "fetch_available_centers": {
        "task": "cowin18.fetch_available_centers",
        "schedule": crontab(minute="*/30"),
    }
}

app.autodiscover_tasks()
