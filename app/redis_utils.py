import json
from datetime import datetime

import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def store_ob_in_redis(site, data):
    ttl = calculate_ttl()
    return redis_client.set(site, json.dumps(data), ex=ttl)


def is_site_in_redis(site):
    return redis_client.exists(site)


def get_ob_from_redis(site):
    return json.loads(redis_client.get(site))


def calculate_ttl():
    current_minute = datetime.now().minute
    return (60 - current_minute) * 60
