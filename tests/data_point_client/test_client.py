from datetime import datetime

import pytest
import requests
import requests_mock

from app.datapoint_client.errors import SiteError
from tests.json_response_fixtures.all_obs_for_invalid_site import obs_json_invalid_site
from tests.json_response_fixtures.all_obs_for_site import obs_json


def test_get_all_obs_json_hits_the_correct_endpoint(client):
    site = 1000

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json={"status": "success"}
        )

        client._get_all_obs_json(site)

    assert m.called


def test_get_all_obs_json_raises_an_error_for_400_or_500_status_codes(client):
    site = 1000

    with pytest.raises(requests.exceptions.HTTPError) as e, requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
             status_code=403
        )

        client._get_all_obs_json(site)

    assert e.value.response.status_code == 403
    assert '403 Client Error' in str(e.value)
    assert m.called


def test_get_all_obs_for_site_returns_an_entry_for_each_ob_in_the_expected_format(client):
    site = 3772

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json=obs_json
        )
        result = client.get_all_obs_for_site(site)

    assert len(result) == 3
    assert result.keys() == {datetime(2018, 3, 2, 23, 0), datetime(2018, 3, 3, 0, 0), datetime(2018, 3, 3, 1, 0)}
    assert result[datetime(2018, 3, 3, 0, 0)] == {
        'W': '8', 'S': '9', 'Pt': 'F', 'P': '992', 'V': '2700', 'Dp': '-0.2', 'H': '95.0', 'T': '0.5', 'D': 'ENE'
    }


def test_get_all_obs_for_site_raises_error_for_invalid_site_id(client):
    site = 0

    with pytest.raises(SiteError) as e, requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json=obs_json_invalid_site
        )
        client.get_all_obs_for_site(site)

    assert e.type == SiteError
    assert str(e.value) == 'Site ID used is not valid'
