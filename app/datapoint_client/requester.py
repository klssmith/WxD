import json
import redis
import requests
from datetime import datetime


class Requester:
    '''
    Decides which sub-requester to should handle the request
    '''
    def __init__(self, api_key):
        self.redis_requester = RedisRequester()
        self.external_requester = ExternalRequester(api_key)

    def get_obs(self, site):
        data = self.redis_requester.get_obs(site) or self.external_requester.get_obs(site)
        self.redis_requester.store_ob(site, data)

        return data

    def get_obs(self, site):
        cached_data = self.redis_requester.get_obs(site)
        if cached_data:
            # cached_data is None if the data is not in redis
            return cached_data

        fresh_data = self.external_requester.get_obs(site)
        self.redis_requester.store_ob(site, fresh_data)
        return fresh_data

    def get_3hourly_forecasts(self, site):
        return self.external_requester.get_3hourly_forecasts(site)


class ExternalRequester:
    '''
    Gets the data from the metoffice
    '''
    BASE_URL = "http://datapoint.metoffice.gov.uk/public/data/"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_obs(self, site):
        url, payload = self._build_url_and_payload('hourly', 'wxobs', site)
        return self._make_request(url, payload)

    def get_3hourly_forecasts(self, site):
        url, payload = self._build_url_and_payload('3hourly', 'wxfcs', site)
        return self._make_request(url, payload)

    def _build_url_and_payload(self, res, type, site):
        url = self.BASE_URL + 'val/{}/all/json/{}'.format(type, site)
        payload = {'key': self.api_key, 'res': res}

        return (url, payload)

    def _make_request(self, url, payload):
        r = requests.get(url, params=payload)

        r.raise_for_status()
        return r.json()


class RedisRequester:
    '''
    Gets the data from the cache
    '''
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def get_obs(self, site):
        data = self.redis_client.get(site)
        if data:
            return json.loads(data)

    def store_ob(self, key, value):
        if not self.redis_client.exists(key):
            current_minute = datetime.now().minute
            ttl = (60 - current_minute) * 60
            self.redis_client.set(key, json.dumps(value), ex=ttl)

    def store_ob(self, key, value):
        current_minute = datetime.now().minute
        ttl = (60 - current_minute) * 60
        self.redis_client.set(key, json.dumps(value), ex=ttl)
