import pytest
import requests
import requests_mock

from app.datapoint_client.client import DatapointClient
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


def test_get_all_obs_for_site_raises_an_error_for_invalid_sites(dp_client):
    data = {'SiteRep': {'DV': {'dataDate': '2019-04-16T08:00:00Z', 'type': 'Obs'}}}
    site = 1000

    with pytest.raises(SiteError) as e, requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, dp_client.api_key),
            json=data,
        )

        dp_client.get_all_obs_for_site(1000)
        assert str(e.value) == 'Site ID used is not valid'


def test_get_all_obs_for_site_calls_formatter(mocker):
    mock_formatter = mocker.Mock()
    client = DatapointClient(api_key='123', formatter=mock_formatter)
    site = 1000
    data = {
        'SiteRep': {'DV': {'Location': {'Period': ['SUNNY ☀️']}}}
    }

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json=data,
        )

        client.get_all_obs_for_site(site)

    mock_formatter.assert_called_once()
