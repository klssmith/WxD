from app.datapoint_client.errors import SiteError
from app.datapoint_client.formatter import ObsFormatter, WeatherFormatter
# from app.datapoint_client.requester import Requester
from app.datapoint_client.requesters import CacheRequester


def validate_site(data):
    # TODO:  The error message isn't accurate - the site may exist but nto have any data
    if not data['SiteRep']['DV'].get('Location'):
        raise SiteError('Site ID used is not valid')


class DatapointClient:
    def __init__(self, api_key, obsformatter=ObsFormatter, wxformatter=WeatherFormatter):
        self.obs_formatter = obsformatter()
        self.wx_formatter = wxformatter()
        self.api_key = api_key
        self.cache_requester = CacheRequester(api_key)

    def get_obs_for_site(self, site):
        raise Exception()
        obs_json = self.cache_requester.get_obs(site)
        validate_site(obs_json)

        return self.format_data(obs_json, self.obs_formatter)

    def get_3hourly_forecasts_for_site(self, site):
        forecast_json = self.cache_requester.get_3hourly_forecasts(site)
        validate_site(forecast_json)

        return self.format_data(forecast_json, self.wx_formatter)

    def format_data(self, data, formatter):
        data = data['SiteRep']['DV']['Location']['Period']
        return formatter.format(data)
