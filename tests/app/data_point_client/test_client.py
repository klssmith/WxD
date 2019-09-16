from datetime import datetime

import pytest
import requests
import requests_mock
import pytz

from app.datapoint_client.client import DatapointClient, ObsFormatter, WeatherFormatter, validate_site
from app.datapoint_client.errors import SiteError
from tests.json_fixtures.all_obs_for_site import obs_json
from tests.json_fixtures.forecast_for_site import three_hourly_fx_json


def test_validate_site_when_site_is_valid_does_not_raise_error():
    valid_data = {'SiteRep': {'DV': {'Location': ['London']}}}

    validate_site(valid_data)


def test_validate_site_with_invalid_site_raises_an_error():
    invalid_data = {'SiteRep': {'DV': {'Something unexpected': ['Manchester']}}}

    with pytest.raises(SiteError) as e:
        validate_site(invalid_data)

    assert str(e.value) == 'Site ID used is not valid'


def test_get_obs_for_site(mocker, site):
    mocker.patch('app.datapoint_client.client.CacheRequester.get_obs', return_value=obs_json)
    mocker.patch.object(ObsFormatter, 'format', return_value='formatted data')

    client = DatapointClient('123')
    assert client.get_obs_for_site(site.id) == 'formatted data'


def test_get_3hourly_forecasts_for_site(mocker, site):
    mocker.patch('app.datapoint_client.client.CacheRequester.get_3hourly_forecasts', return_value=three_hourly_fx_json)
    mocker.patch.object(WeatherFormatter, 'format', return_value='formatted data')

    client = DatapointClient('123')
    assert client.get_3hourly_forecasts_for_site(site.id) == 'formatted data'


def test_datapoint_client_format_data(mocker):
    formatter = mocker.Mock()
    client = DatapointClient('123')
    data = {'SiteRep': {'DV': {'Location': {'Period': 'my_weather'}}}}

    client.format_data(data, formatter)

    assert len(formatter.method_calls) == 1
    assert formatter.method_calls[0] == mocker.call.format('my_weather')


# CLIENT FEATURE TESTS
def test_feature_get_obs_for_site(mocker):
    mocker.patch('app.datapoint_client.requesters.redis.Redis.get', return_value=None)

    site = 1000
    client = DatapointClient('123')

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json=obs_json,
        )

        observations = client.get_obs_for_site(site)
        assert len(observations) == 3
        assert observations[datetime(2018, 3, 2, 23, 0, tzinfo=pytz.utc)] == {
            'Wind Direction': 'E',
            'Screen Relative Humidity': '94.4',
            'Pressure': '992',
            'Wind Speed': '11',
            'Temperature': '0.3',
            'Visibility': '3200',
            'Weather Type': 'Mist',
            'Pressure Tendency': 'Rising',
            'Dew Point': '-0.5'}


def test_feature_get_3hourly_forecasts_for_site(mocker):
    mocker.patch('app.datapoint_client.requesters.redis.Redis.get', return_value=None)

    site = 1000
    client = DatapointClient('123')

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{}?res=3hourly&key={}'.format(
             site, client.api_key),
            json=three_hourly_fx_json,
        )

        forecasts = client.get_3hourly_forecasts_for_site(site)
        assert len(forecasts) == 3
        assert forecasts[datetime(2019, 4, 28, 18, 0, tzinfo=pytz.utc)] == {
            'Wind Direction': 'NNE',
            'Feels Like Temperature': '12',
            'Wind Gust': '16',
            'Screen Relative Humidity': '58',
            'Precipitation Probability': '0',
            'Wind Speed': '11',
            'Temperature': '14',
            'Visibility': 'Good - Between 10-20 km',
            'Weather Type': 'Partly cloudy (day)',
            'Max UV Index': '1'}
