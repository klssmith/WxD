from datetime import datetime

import pytest
import requests
import requests_mock

from app.datapoint_client.client import DatapointClient, validate_site
from app.datapoint_client.errors import SiteError
from tests.json_fixtures.all_obs_for_site import obs_json


def test_validate_site_when_site_is_valid_does_not_raise_error():
    valid_data = {'SiteRep': {'DV': {'Location': ['London']}}}

    validate_site(valid_data)


def test_validate_site_with_invalid_site_raises_an_error():
    invalid_data = {'SiteRep': {'DV': {'Something unexpected': ['Manchester']}}}

    with pytest.raises(SiteError) as e:
        validate_site(invalid_data)

    assert str(e.value) == 'Site ID used is not valid'


def test_datapoint_client_build_url_and_payload(mocker):
    client = DatapointClient('123', mocker.Mock())
    url, payload = client.build_url_and_payload('hourly', 'wxfcs', 1000)

    assert url == client.BASE_URL + 'val/wxfcs/all/json/1000'
    assert payload == {'key': client.api_key, 'res': 'hourly'}


def test_datapoint_client_make_request(mocker):
    client = DatapointClient('123', mocker.Mock())
    url = 'http://www.example.com'
    payload = {'key': client.api_key, 'res': 'hourly'}

    with requests_mock.Mocker() as m:
        m.get(
            '{url}?key={api_key}&res={res}'.format(url=url, api_key=payload['key'], res=payload['res']),
            complete_qs=True,
            json="the weather"
        )
        response = client.make_request('http://www.example.com/', payload)

    assert response == 'the weather'


def test_datapoint_client_make_request_when_bad_status_code_returned(mocker):
    client = DatapointClient('123', mocker.Mock())
    url = 'http://www.example.com'
    payload = {'key': client.api_key, 'res': 'hourly'}

    with pytest.raises(requests.exceptions.HTTPError) as e, requests_mock.Mocker() as m:
        m.get(
            '{url}?key={api_key}&res={res}'.format(url=url, api_key=payload['key'], res=payload['res']),
            complete_qs=True,
            status_code=403
        )
        client.make_request('http://www.example.com/', payload)

    assert m.called
    assert '403 Client Error' in str(e.value)


def test_datapoint_client_format_data(mocker):
    formatter = mocker.Mock()
    client = DatapointClient('123', formatter)
    data = {'SiteRep': {'DV': {'Location': {'Period': 'my_weather'}}}}

    client.format_data(data, formatter)

    assert len(formatter.method_calls) == 1
    assert formatter.method_calls[0] == mocker.call.format('my_weather')


def test_get_obs_for_site(mocker):
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
        assert observations[datetime(2018, 3, 2, 23, 0)] == {
            'Wind Direction': 'E',
            'Screen Relative Humidity': '94.4',
            'Pressure': '992',
            'Wind Speed': '11',
            'Temperature': '0.3',
            'Visibility': '3200',
            'Weather Type': 'Mist',
            'Pressure Tendency': 'Rising',
            'Dew Point': '-0.5'}
