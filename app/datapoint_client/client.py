import requests

from app.datapoint_client.errors import SiteError
from app.datapoint_client.obs_formatter import format_observations


class DatapointClient:
    BASE_URL = "http://datapoint.metoffice.gov.uk/public/data/"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_all_obs_for_site(self, site):
        obs_json = self._get_all_obs_json(site)
        formatted_obs = self._validate_site_and_format_obs(obs_json)

        return formatted_obs

    def _get_all_obs_json(self, site):
        """
        Returns the JSON from this endoint:
        http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/<site>?res=hourly&key=<API key>
        """
        payload = {'key': self.api_key, 'res': 'hourly'}
        url = self.BASE_URL + 'val/wxobs/all/json/{}'.format(site)
        r = requests.get(url, params=payload)

        r.raise_for_status()
        return r.json()

    def _validate_site_and_format_obs(self, data):
        if data['SiteRep']['DV'].get('Location'):
            data = data['SiteRep']['DV']['Location']['Period']
        else:
            raise SiteError('Site ID used is not valid')

        return format_observations(data)
