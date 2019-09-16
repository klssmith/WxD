import json
import redis
import requests
from datetime import datetime


class ExternalRequester:
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


class CacheRequester:
    def __init__(self, api_key, external_requester=ExternalRequester):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.external_requester = external_requester(api_key)

    def get_obs(self, site):
        # breakpoint()
        data = self.redis_client.get(site)
        if data:
            return json.loads(data)

        return self._get_obs_from_external_requester(site)

    def get_3hourly_forecasts(self, site):
        return self.external_requester.get_3hourly_forecasts(site)

    def _get_obs_from_external_requester(self, site):
        data = self.external_requester.get_obs(site)
        self._store(site, data)

        return data

    def _store(self, key, value):
        current_minute = datetime.now().minute
        ttl = (60 - current_minute) * 60
        self.redis_client.set(key, json.dumps(value), ex=ttl)
