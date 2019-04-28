import requests

from app.datapoint_client.errors import SiteError
from app.datapoint_client.formatter import ObsFormatter, WeatherFormatter


def validate_site(data):
    if not data['SiteRep']['DV'].get('Location'):
        raise SiteError('Site ID used is not valid')


class DatapointClient:
    BASE_URL = "http://datapoint.metoffice.gov.uk/public/data/"

    def __init__(self, api_key, obsformatter=ObsFormatter, wxformatter=WeatherFormatter):
        self.api_key = api_key
        self.obs_formatter = obsformatter()
        self.wx_formatter = wxformatter()

    def get_obs_for_site(self, site):
        url, payload = self.build_url_and_payload('hourly', 'wxobs', site)
        obs_json = self.make_request(url, payload)
        validate_site(obs_json)

        return self.format_data(obs_json, self.obs_formatter)

    def get_3hourly_forecasts_for_site(self, site):
        url, payload = self.build_url_and_payload('3hourly', 'wxfcs', site)
        forecast_json = self.make_request(url, payload)
        validate_site(forecast_json)

        return self.format_data(forecast_json, self.wx_formatter)

    def build_url_and_payload(self, res, type, site):
        url = self.BASE_URL + 'val/{}/all/json/{}'.format(type, site)
        payload = {'key': self.api_key, 'res': res}

        return (url, payload)

    def make_request(self, url, payload):
        r = requests.get(url, params=payload)

        r.raise_for_status()
        return r.json()

    def format_data(self, data, formatter):
        data = data['SiteRep']['DV']['Location']['Period']
        return formatter.format(data)
