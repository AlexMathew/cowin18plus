import os

from .redis import Redis

redis = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
