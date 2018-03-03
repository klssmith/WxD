from collections import OrderedDict
from datetime import datetime

import requests

from app.datapoint_client.errors import SiteError


class DatapointClient:
    BASE_URL = "http://datapoint.metoffice.gov.uk/public/data/"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_all_obs_for_site(self, site):
        obs_json = self._get_all_obs_json(site)
        formatted_obs = self._format_obs_data(obs_json)

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

    def _format_obs_data(self, data):
        """
        Convert the JSON response into an OrderedDict containing the datetime as the key.
        """
        if data['SiteRep']['DV'].get('Location'):
            data = data['SiteRep']['DV']['Location']['Period']
        else:
            raise SiteError('Site ID used is not valid')

        od = OrderedDict()

        for day_dict in data:
            day = day_dict['value']
            for hour_dict in day_dict['Rep']:
                hour_dict_copy = hour_dict.copy()

                mins = int(hour_dict['$']) // 60
                dt = datetime(
                    int(day[0:4]),
                    int(day[5:7]),
                    int(day[8:10]),
                    mins
                )
                del hour_dict_copy['$']
                od[dt] = hour_dict_copy

        return od
