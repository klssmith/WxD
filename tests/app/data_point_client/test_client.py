import pytest
import requests
import requests_mock

from app.datapoint_client.errors import SiteError


def test_get_all_obs_json_hits_the_correct_endpoint(dp_client):
    site = 1000

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, dp_client.api_key),
            json={"status": "success"}
        )

        dp_client._get_all_obs_json(site)

    assert m.called


def test_get_all_obs_json_raises_an_error_for_400_or_500_status_codes(dp_client):
    site = 1000

    with pytest.raises(requests.exceptions.HTTPError) as e, requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, dp_client.api_key),
            status_code=403
        )

        dp_client._get_all_obs_json(site)

    assert e.value.response.status_code == 403
    assert '403 Client Error' in str(e.value)
    assert m.called


def test_validate_site_and_format_obs_calls_format_observations_function(mocker, dp_client):
    data = {
        'SiteRep': {
            'Wx': {'Param': []},
            'DV': {
                'type': 'Obs',
                'Location': {'name': 'HEATHROW', 'Period': [], 'type': 'Day', 'value': '2018-03-15Z'},
                'lat': '51.479',
                'i': '3772',
                'country': 'ENGLAND',
                'elevation': '25.0',
                'continent': 'EUROPE',
                'lon': '-0.449'
            },
            'dataDate': '2018-03-15T19:00:00Z'
        }
    }

    m = mocker.patch('app.datapoint_client.client.format_observations')
    dp_client._validate_site_and_format_obs(data)

    m.assert_called_once_with([])


def test_validate_site_and_format_obs_raises_error_with_invalid_site_id(dp_client):
    data = {'SiteRep': {'DV': {'dataDate': '2018-03-15T19:00:00Z', 'type': 'Obs'}, 'Wx': {'Param': []}}}

    with pytest.raises(SiteError) as e:
        dp_client._validate_site_and_format_obs(data)

    assert e.type == SiteError
    assert str(e.value) == 'Site ID used is not valid'
